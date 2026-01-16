"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ — LOAD TESTING SUITE (K6)
Q1 2026 - Week 8: Testing Excellence
═══════════════════════════════════════════════════════════════════════════════

Suite complète de load testing pour CHE·NU™.
Target: 1000+ VUs, <200ms p95, 0% errors

Créé: 20 Décembre 2025
Version: v41.4
"""

import http from 'k6/http'
import { check, sleep, group } from 'k6'
import { Rate, Trend, Counter } from 'k6/metrics'
import { randomString, randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js'

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000'
const GRAPHQL_URL = `${BASE_URL}/graphql`

// Test users
const USERS = JSON.parse(open('./test-users.json'))

// ═══════════════════════════════════════════════════════════════════════════
// CUSTOM METRICS
// ═══════════════════════════════════════════════════════════════════════════

const errorRate = new Rate('errors')
const cacheHitRate = new Rate('cache_hits')
const apiDuration = new Trend('api_duration')
const threadCreationTime = new Trend('thread_creation_time')
const loginAttempts = new Counter('login_attempts')

// ═══════════════════════════════════════════════════════════════════════════
// TEST SCENARIOS
// ═══════════════════════════════════════════════════════════════════════════

export const options = {
  scenarios: {
    // Smoke test: 1 user for 1 minute
    smoke: {
      executor: 'constant-vus',
      vus: 1,
      duration: '1m',
      tags: { test_type: 'smoke' },
      exec: 'smokeTest'
    },
    
    // Load test: Ramp up to 100 users
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },   // Ramp up to 50
        { duration: '5m', target: 50 },   // Stay at 50
        { duration: '2m', target: 100 },  // Ramp up to 100
        { duration: '5m', target: 100 },  // Stay at 100
        { duration: '2m', target: 0 },    // Ramp down
      ],
      tags: { test_type: 'load' },
      exec: 'loadTest'
    },
    
    // Stress test: Push to breaking point
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 300 },
        { duration: '5m', target: 300 },
        { duration: '2m', target: 400 },
        { duration: '5m', target: 400 },
        { duration: '10m', target: 0 },
      ],
      tags: { test_type: 'stress' },
      exec: 'stressTest'
    },
    
    // Spike test: Sudden traffic surge
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 100 },  // Quick ramp
        { duration: '1m', target: 100 },
        { duration: '10s', target: 1000 }, // SPIKE!
        { duration: '3m', target: 1000 },
        { duration: '10s', target: 100 },  // Drop
        { duration: '3m', target: 100 },
        { duration: '10s', target: 0 },
      ],
      tags: { test_type: 'spike' },
      exec: 'spikeTest'
    },
    
    // Soak test: Sustained load for extended period
    soak: {
      executor: 'constant-vus',
      vus: 50,
      duration: '4h',
      tags: { test_type: 'soak' },
      exec: 'soakTest'
    }
  },
  
  // Thresholds
  thresholds: {
    // HTTP errors should be less than 1%
    'errors': ['rate<0.01'],
    
    // 95% of requests should be below 200ms
    'http_req_duration': ['p(95)<200'],
    
    // API duration p95 < 100ms
    'api_duration': ['p(95)<100'],
    
    // Cache hit rate should be > 60%
    'cache_hits': ['rate>0.6'],
    
    // Thread creation < 500ms
    'thread_creation_time': ['p(95)<500']
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

function getRandomUser() {
  return USERS[Math.floor(Math.random() * USERS.length)]
}

function login(email, password) {
  const response = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify({
    email,
    password
  }), {
    headers: { 'Content-Type': 'application/json' }
  })
  
  loginAttempts.add(1)
  
  check(response, {
    'login successful': (r) => r.status === 200,
    'token received': (r) => r.json('access_token') !== undefined
  })
  
  return response.json('access_token')
}

function makeAuthRequest(url, token, method = 'GET', body = null) {
  const params = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }
  
  const start = new Date()
  
  const response = method === 'GET'
    ? http.get(url, params)
    : http.post(url, body ? JSON.stringify(body) : null, params)
  
  const duration = new Date() - start
  apiDuration.add(duration)
  
  // Check cache header
  if (response.headers['X-Cache']) {
    cacheHitRate.add(response.headers['X-Cache'] === 'HIT' ? 1 : 0)
  }
  
  return response
}

function graphqlQuery(query, variables, token) {
  const response = http.post(GRAPHQL_URL, JSON.stringify({
    query,
    variables
  }), {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  
  check(response, {
    'graphql success': (r) => r.status === 200,
    'no errors': (r) => !r.json('errors')
  })
  
  return response
}

// ═══════════════════════════════════════════════════════════════════════════
// SMOKE TEST (Sanity check)
// ═══════════════════════════════════════════════════════════════════════════

export function smokeTest() {
  const user = USERS[0]
  const token = login(user.email, user.password)
  
  if (!token) {
    errorRate.add(1)
    return
  }
  
  group('Health Checks', () => {
    // Database health
    const dbHealth = http.get(`${BASE_URL}/health/database`)
    check(dbHealth, {
      'database healthy': (r) => r.status === 200 && r.json('status') === 'healthy'
    })
    
    // API health
    const apiHealth = http.get(`${BASE_URL}/health`)
    check(apiHealth, {
      'api healthy': (r) => r.status === 200
    })
  })
  
  group('Basic Functionality', () => {
    // Get user
    const userResponse = makeAuthRequest(`${BASE_URL}/api/v1/users/me`, token)
    check(userResponse, {
      'user retrieved': (r) => r.status === 200
    })
    
    // Get threads
    const threadsResponse = makeAuthRequest(`${BASE_URL}/api/v1/threads`, token)
    check(threadsResponse, {
      'threads retrieved': (r) => r.status === 200
    })
  })
  
  sleep(1)
}

// ═══════════════════════════════════════════════════════════════════════════
// LOAD TEST (Normal traffic)
// ═══════════════════════════════════════════════════════════════════════════

export function loadTest() {
  const user = getRandomUser()
  const token = login(user.email, user.password)
  
  if (!token) {
    errorRate.add(1)
    return
  }
  
  // Simulate user behavior
  group('User Journey', () => {
    // 1. View threads (90% of users)
    if (Math.random() < 0.9) {
      const threads = makeAuthRequest(`${BASE_URL}/api/v1/threads`, token)
      check(threads, {
        'threads loaded': (r) => r.status === 200,
        'response time OK': (r) => r.timings.duration < 200
      })
      
      sleep(randomIntBetween(1, 3))
    }
    
    // 2. View specific thread (70% of users)
    if (Math.random() < 0.7) {
      const threadId = randomString(10)
      const thread = makeAuthRequest(`${BASE_URL}/api/v1/threads/${threadId}`, token)
      check(thread, {
        'thread loaded': (r) => r.status === 200 || r.status === 404
      })
      
      sleep(randomIntBetween(2, 5))
    }
    
    // 3. Create thread (30% of users)
    if (Math.random() < 0.3) {
      const start = new Date()
      
      const newThread = makeAuthRequest(
        `${BASE_URL}/api/v1/threads`,
        token,
        'POST',
        {
          title: `Test Thread ${randomString(8)}`,
          description: 'Load test thread',
          sphere: 'personal'
        }
      )
      
      const duration = new Date() - start
      threadCreationTime.add(duration)
      
      check(newThread, {
        'thread created': (r) => r.status === 201,
        'creation fast': (r) => r.timings.duration < 500
      })
      
      sleep(randomIntBetween(1, 2))
    }
    
    // 4. GraphQL query (50% of users)
    if (Math.random() < 0.5) {
      const query = `
        query {
          user {
            id
            email
            threads(limit: 10) {
              id
              title
              lastMessage
            }
          }
        }
      `
      
      const gql = graphqlQuery(query, {}, token)
      check(gql, {
        'graphql success': (r) => r.status === 200,
        'graphql fast': (r) => r.timings.duration < 150
      })
      
      sleep(randomIntBetween(1, 3))
    }
  })
  
  // Think time
  sleep(randomIntBetween(3, 10))
}

// ═══════════════════════════════════════════════════════════════════════════
// STRESS TEST (Push to limits)
// ═══════════════════════════════════════════════════════════════════════════

export function stressTest() {
  const user = getRandomUser()
  const token = login(user.email, user.password)
  
  if (!token) {
    errorRate.add(1)
    return
  }
  
  // Aggressive user behavior
  group('Stress Operations', () => {
    // Rapid thread creation
    for (let i = 0; i < 3; i++) {
      makeAuthRequest(
        `${BASE_URL}/api/v1/threads`,
        token,
        'POST',
        {
          title: `Stress Test ${randomString(8)}`,
          sphere: 'personal'
        }
      )
    }
    
    // Parallel requests
    const requests = http.batch([
      ['GET', `${BASE_URL}/api/v1/threads`, null, { headers: { 'Authorization': `Bearer ${token}` } }],
      ['GET', `${BASE_URL}/api/v1/users/me`, null, { headers: { 'Authorization': `Bearer ${token}` } }],
      ['GET', `${BASE_URL}/api/v1/agents`, null, { headers: { 'Authorization': `Bearer ${token}` } }],
    ])
    
    check(requests, {
      'all requests successful': (r) => r.every(res => res.status === 200)
    })
  })
  
  sleep(randomIntBetween(1, 3))
}

// ═══════════════════════════════════════════════════════════════════════════
// SPIKE TEST (Traffic surge)
// ═══════════════════════════════════════════════════════════════════════════

export function spikeTest() {
  // Same as load test but with minimal think time
  loadTest()
  sleep(randomIntBetween(0, 1)) // Very short think time
}

// ═══════════════════════════════════════════════════════════════════════════
// SOAK TEST (Sustained load)
// ═══════════════════════════════════════════════════════════════════════════

export function soakTest() {
  // Same as load test but runs for 4 hours
  loadTest()
}

// ═══════════════════════════════════════════════════════════════════════════
// TEARDOWN
// ═══════════════════════════════════════════════════════════════════════════

export function teardown(data) {
  // Cleanup if needed
  console.log('Test completed')
}

// ═══════════════════════════════════════════════════════════════════════════
// TEST DATA FILE
// ═══════════════════════════════════════════════════════════════════════════

/*
// test-users.json

[
  {
    "email": "user1@chenu.test",
    "password": "TestPassword123!"
  },
  {
    "email": "user2@chenu.test",
    "password": "TestPassword123!"
  },
  {
    "email": "user3@chenu.test",
    "password": "TestPassword123!"
  }
]
*/

// ═══════════════════════════════════════════════════════════════════════════
// RUNNING TESTS
// ═══════════════════════════════════════════════════════════════════════════

/*
INSTALLATION:
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

RUN TESTS:
# Smoke test
k6 run --env BASE_URL=http://localhost:8000 load-test.js --include-system-env-vars

# Load test
k6 run --out json=results.json load-test.js

# Cloud (k6 Cloud)
k6 cloud load-test.js

# With InfluxDB output
k6 run --out influxdb=http://localhost:8086/k6 load-test.js

# Custom scenario
k6 run --env BASE_URL=https://staging.chenu.com \
       --duration 10m \
       --vus 50 \
       load-test.js

ANALYZE RESULTS:
k6 run --out json=results.json load-test.js
# Then use k6-reporter or custom scripts
*/

// ═══════════════════════════════════════════════════════════════════════════
// EXPECTED RESULTS
// ═══════════════════════════════════════════════════════════════════════════

/*
TARGETS:

Smoke Test:
✅ 100% success rate
✅ All health checks pass

Load Test (100 VUs):
✅ <1% error rate
✅ p95 < 200ms
✅ Cache hit rate > 60%
✅ Thread creation < 500ms

Stress Test (400 VUs):
✅ <5% error rate
✅ p95 < 500ms
✅ No crashes
✅ Graceful degradation

Spike Test (1000 VUs):
✅ <10% error rate during spike
✅ System recovers after spike
✅ No data loss

Soak Test (4 hours):
✅ No memory leaks
✅ Stable performance
✅ No degradation over time
*/
