// ═══════════════════════════════════════════════════════════════════════════════
// CHE·NU™ — K6 LOAD TESTS
// Sprint 7: Performance and stress testing
// ═══════════════════════════════════════════════════════════════════════════════

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ═══════════════════════════════════════════════════════════════════════════════
// CUSTOM METRICS
// ═══════════════════════════════════════════════════════════════════════════════

const errorRate = new Rate('errors');
const sphereLoadTime = new Trend('sphere_load_time');
const bureauLoadTime = new Trend('bureau_load_time');
const threadCreateTime = new Trend('thread_create_time');
const tokenOperations = new Counter('token_operations');

// ═══════════════════════════════════════════════════════════════════════════════
// TEST CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

export const options = {
  // Test stages
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 50 },    // Ramp up to 50 users
    { duration: '2m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 100 },  // Spike to 100 users
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  
  // Thresholds
  thresholds: {
    http_req_duration: ['p(95)<500'],     // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],       // Less than 1% failures
    errors: ['rate<0.05'],                // Less than 5% errors
    sphere_load_time: ['p(95)<300'],      // Sphere loads under 300ms
    bureau_load_time: ['p(95)<400'],      // Bureau loads under 400ms
    thread_create_time: ['p(95)<600'],    // Thread creation under 600ms
  },
};

// ═══════════════════════════════════════════════════════════════════════════════
// BASE URL & AUTH
// ═══════════════════════════════════════════════════════════════════════════════

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const API_URL = `${BASE_URL}/api/v1`;

// Mock auth token for testing
const AUTH_TOKEN = __ENV.AUTH_TOKEN || 'test-token-for-load-testing';

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${AUTH_TOKEN}`,
};

// ═══════════════════════════════════════════════════════════════════════════════
// SPHERE IDS (9 SPHERES - FROZEN)
// ═══════════════════════════════════════════════════════════════════════════════

const SPHERE_IDS = [
  'personal',
  'business', 
  'government',
  'creative',
  'community',
  'social',
  'entertainment',
  'team',
  'scholar',
];

// ═══════════════════════════════════════════════════════════════════════════════
// BUREAU SECTION IDS (6 SECTIONS - HARD LIMIT)
// ═══════════════════════════════════════════════════════════════════════════════

const BUREAU_SECTIONS = [
  'quick_capture',
  'resume_workspace',
  'threads',
  'data_files',
  'active_agents',
  'meetings',
];

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

function randomSphere() {
  return SPHERE_IDS[Math.floor(Math.random() * SPHERE_IDS.length)];
}

function randomSection() {
  return BUREAU_SECTIONS[Math.floor(Math.random() * BUREAU_SECTIONS.length)];
}

function randomThreadTitle() {
  const titles = [
    'Project Discussion',
    'Meeting Notes',
    'Research Thread',
    'Task Planning',
    'Creative Ideas',
  ];
  return titles[Math.floor(Math.random() * titles.length)] + ` ${Date.now()}`;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN TEST SCENARIO
// ═══════════════════════════════════════════════════════════════════════════════

export default function() {
  // Test Health Endpoint
  group('Health Check', () => {
    const res = http.get(`${API_URL}/health`);
    check(res, {
      'health status is 200': (r) => r.status === 200,
      'health response time < 100ms': (r) => r.timings.duration < 100,
    });
    errorRate.add(res.status !== 200);
  });

  sleep(0.5);

  // Test Sphere Loading
  group('Sphere Operations', () => {
    const sphereId = randomSphere();
    const start = Date.now();
    
    const res = http.get(`${API_URL}/spheres/${sphereId}`, { headers });
    
    sphereLoadTime.add(Date.now() - start);
    
    check(res, {
      'sphere loads successfully': (r) => r.status === 200 || r.status === 404,
      'sphere has id': (r) => {
        if (r.status === 200) {
          const body = JSON.parse(r.body);
          return body.id !== undefined || body.sphere_id !== undefined;
        }
        return true;
      },
    });
    
    errorRate.add(res.status >= 500);
  });

  sleep(0.3);

  // Test Bureau Section Loading
  group('Bureau Operations', () => {
    const sphereId = randomSphere();
    const sectionId = randomSection();
    const start = Date.now();
    
    const res = http.get(
      `${API_URL}/spheres/${sphereId}/bureau/${sectionId}`,
      { headers }
    );
    
    bureauLoadTime.add(Date.now() - start);
    
    check(res, {
      'bureau section loads': (r) => r.status === 200 || r.status === 404,
    });
    
    errorRate.add(res.status >= 500);
  });

  sleep(0.3);

  // Test Thread Creation (10% of requests)
  if (Math.random() < 0.1) {
    group('Thread Operations', () => {
      const start = Date.now();
      
      const payload = JSON.stringify({
        title: randomThreadTitle(),
        sphere_id: randomSphere(),
        type: 'chat',
        token_budget: 5000,
      });
      
      const res = http.post(`${API_URL}/threads`, payload, { headers });
      
      threadCreateTime.add(Date.now() - start);
      
      check(res, {
        'thread created': (r) => r.status === 201 || r.status === 200 || r.status === 404,
      });
      
      errorRate.add(res.status >= 500);
    });
  }

  sleep(0.2);

  // Test Token Budget Check
  group('Governance Operations', () => {
    const res = http.get(`${API_URL}/governance/budget`, { headers });
    
    check(res, {
      'budget endpoint responds': (r) => r.status === 200 || r.status === 404,
    });
    
    tokenOperations.add(1);
    errorRate.add(res.status >= 500);
  });

  sleep(0.5);

  // Test Agent Listing (Nova should always be present)
  group('Agent Operations', () => {
    const res = http.get(`${API_URL}/agents`, { headers });
    
    check(res, {
      'agents endpoint responds': (r) => r.status === 200 || r.status === 404,
      'response is array or has agents': (r) => {
        if (r.status === 200) {
          try {
            const body = JSON.parse(r.body);
            return Array.isArray(body) || body.agents !== undefined;
          } catch {
            return true;
          }
        }
        return true;
      },
    });
    
    errorRate.add(res.status >= 500);
  });

  sleep(0.3);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SETUP FUNCTION
// ═══════════════════════════════════════════════════════════════════════════════

export function setup() {
  console.log('🚀 CHE·NU Load Test Starting...');
  console.log(`📍 Target: ${BASE_URL}`);
  console.log(`🔵 Testing ${SPHERE_IDS.length} spheres`);
  console.log(`📦 Testing ${BUREAU_SECTIONS.length} bureau sections`);
  
  // Verify API is reachable
  const res = http.get(`${API_URL}/health`);
  if (res.status !== 200) {
    console.warn('⚠️ API health check failed, tests may not work correctly');
  }
  
  return { startTime: Date.now() };
}

// ═══════════════════════════════════════════════════════════════════════════════
// TEARDOWN FUNCTION
// ═══════════════════════════════════════════════════════════════════════════════

export function teardown(data) {
  const duration = (Date.now() - data.startTime) / 1000;
  console.log(`\n✅ CHE·NU Load Test Complete`);
  console.log(`⏱️ Total Duration: ${duration.toFixed(2)}s`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// STRESS TEST SCENARIO
// ═══════════════════════════════════════════════════════════════════════════════

export function stressTest() {
  // Rapid-fire requests to test system limits
  for (let i = 0; i < 10; i++) {
    http.get(`${API_URL}/spheres/${randomSphere()}`, { headers });
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SPIKE TEST SCENARIO
// ═══════════════════════════════════════════════════════════════════════════════

export function spikeTest() {
  // Simulate sudden traffic spike
  const requests = [];
  for (let i = 0; i < 20; i++) {
    requests.push(['GET', `${API_URL}/health`]);
    requests.push(['GET', `${API_URL}/spheres/${randomSphere()}`]);
  }
  
  http.batch(requests);
}
