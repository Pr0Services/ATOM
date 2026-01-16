"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ — COMPONENT TESTING SUITE (VITEST)
Q1 2026 - Week 7: Testing Excellence
═══════════════════════════════════════════════════════════════════════════════

Suite complète de tests unitaires et d'intégration pour composants React.
Target: 85%+ coverage, instant feedback

Créé: 20 Décembre 2025
Version: v41.4
"""

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { renderHook, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'

// ═══════════════════════════════════════════════════════════════════════════
// SPHERE COMPONENT TESTS
// ═══════════════════════════════════════════════════════════════════════════

import { SphereNavigator } from '../components/SphereNavigator'
import { SphereCard } from '../components/SphereCard'

describe('SphereNavigator', () => {
  const mockSpheres = [
    { id: 'personal', name: 'Personal', icon: '🏠', active: false },
    { id: 'business', name: 'Business', icon: '💼', active: false }
  ]
  
  it('should render all spheres', () => {
    render(<SphereNavigator spheres={mockSpheres} />)
    
    expect(screen.getByText('Personal')).toBeInTheDocument()
    expect(screen.getByText('Business')).toBeInTheDocument()
  })
  
  it('should activate sphere on click', async () => {
    const onSelect = vi.fn()
    render(<SphereNavigator spheres={mockSpheres} onSelect={onSelect} />)
    
    const personalSphere = screen.getByText('Personal')
    await userEvent.click(personalSphere)
    
    expect(onSelect).toHaveBeenCalledWith('personal')
  })
  
  it('should highlight active sphere', () => {
    const activeSpheres = [
      { ...mockSpheres[0], active: true },
      mockSpheres[1]
    ]
    
    render(<SphereNavigator spheres={activeSpheres} />)
    
    const personalCard = screen.getByTestId('sphere-card-personal')
    expect(personalCard).toHaveClass('active')
  })
  
  it('should support keyboard navigation', async () => {
    const onSelect = vi.fn()
    render(<SphereNavigator spheres={mockSpheres} onSelect={onSelect} />)
    
    const personalSphere = screen.getByText('Personal')
    personalSphere.focus()
    
    fireEvent.keyDown(personalSphere, { key: 'Enter' })
    
    expect(onSelect).toHaveBeenCalledWith('personal')
  })
})

describe('SphereCard', () => {
  const sphere = {
    id: 'personal',
    name: 'Personal',
    icon: '🏠',
    color: '#D8B26A',
    count: 5
  }
  
  it('should display sphere information', () => {
    render(<SphereCard sphere={sphere} />)
    
    expect(screen.getByText('Personal')).toBeInTheDocument()
    expect(screen.getByText('🏠')).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
  })
  
  it('should apply custom color', () => {
    render(<SphereCard sphere={sphere} />)
    
    const card = screen.getByTestId('sphere-card-personal')
    expect(card).toHaveStyle({ borderColor: '#D8B26A' })
  })
  
  it('should emit click event', async () => {
    const onClick = vi.fn()
    render(<SphereCard sphere={sphere} onClick={onClick} />)
    
    await userEvent.click(screen.getByText('Personal'))
    
    expect(onClick).toHaveBeenCalledWith('personal')
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// THREAD COMPONENT TESTS
// ═══════════════════════════════════════════════════════════════════════════

import { ThreadList } from '../components/ThreadList'
import { ThreadItem } from '../components/ThreadItem'
import { ThreadComposer } from '../components/ThreadComposer'

describe('ThreadList', () => {
  const mockThreads = [
    {
      id: '1',
      title: 'Test Thread 1',
      lastMessage: 'Hello world',
      timestamp: '2025-12-20T10:00:00Z',
      unread: 2
    },
    {
      id: '2',
      title: 'Test Thread 2',
      lastMessage: 'Another message',
      timestamp: '2025-12-20T11:00:00Z',
      unread: 0
    }
  ]
  
  it('should render thread list', () => {
    render(<ThreadList threads={mockThreads} />)
    
    expect(screen.getByText('Test Thread 1')).toBeInTheDocument()
    expect(screen.getByText('Test Thread 2')).toBeInTheDocument()
  })
  
  it('should show unread count', () => {
    render(<ThreadList threads={mockThreads} />)
    
    const unreadBadge = screen.getByText('2')
    expect(unreadBadge).toBeInTheDocument()
  })
  
  it('should filter threads', async () => {
    render(<ThreadList threads={mockThreads} />)
    
    const searchInput = screen.getByPlaceholderText('Search threads')
    await userEvent.type(searchInput, 'Thread 1')
    
    await waitFor(() => {
      expect(screen.getByText('Test Thread 1')).toBeInTheDocument()
      expect(screen.queryByText('Test Thread 2')).not.toBeInTheDocument()
    })
  })
  
  it('should select thread on click', async () => {
    const onSelect = vi.fn()
    render(<ThreadList threads={mockThreads} onSelect={onSelect} />)
    
    await userEvent.click(screen.getByText('Test Thread 1'))
    
    expect(onSelect).toHaveBeenCalledWith('1')
  })
  
  it('should show empty state', () => {
    render(<ThreadList threads={[]} />)
    
    expect(screen.getByText('No threads yet')).toBeInTheDocument()
  })
})

describe('ThreadComposer', () => {
  it('should allow message input', async () => {
    render(<ThreadComposer />)
    
    const input = screen.getByPlaceholderText('Type a message')
    await userEvent.type(input, 'Hello world')
    
    expect(input).toHaveValue('Hello world')
  })
  
  it('should send message on submit', async () => {
    const onSend = vi.fn()
    render(<ThreadComposer onSend={onSend} />)
    
    const input = screen.getByPlaceholderText('Type a message')
    await userEvent.type(input, 'Test message')
    
    const sendButton = screen.getByText('Send')
    await userEvent.click(sendButton)
    
    expect(onSend).toHaveBeenCalledWith('Test message')
    expect(input).toHaveValue('') // Input cleared
  })
  
  it('should support Enter key to send', async () => {
    const onSend = vi.fn()
    render(<ThreadComposer onSend={onSend} />)
    
    const input = screen.getByPlaceholderText('Type a message')
    await userEvent.type(input, 'Test message{Enter}')
    
    expect(onSend).toHaveBeenCalledWith('Test message')
  })
  
  it('should disable send when empty', () => {
    render(<ThreadComposer />)
    
    const sendButton = screen.getByText('Send')
    expect(sendButton).toBeDisabled()
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// AGENT COMPONENT TESTS
// ═══════════════════════════════════════════════════════════════════════════

import { AgentCard } from '../components/AgentCard'
import { AgentHireModal } from '../components/AgentHireModal'

describe('AgentCard', () => {
  const agent = {
    id: 'nova',
    name: 'Nova',
    role: 'System Intelligence',
    level: 'L0',
    status: 'active'
  }
  
  it('should display agent information', () => {
    render(<AgentCard agent={agent} />)
    
    expect(screen.getByText('Nova')).toBeInTheDocument()
    expect(screen.getByText('System Intelligence')).toBeInTheDocument()
    expect(screen.getByText('L0')).toBeInTheDocument()
  })
  
  it('should show active status', () => {
    render(<AgentCard agent={agent} />)
    
    const statusBadge = screen.getByText('Active')
    expect(statusBadge).toBeInTheDocument()
  })
  
  it('should emit click event', async () => {
    const onClick = vi.fn()
    render(<AgentCard agent={agent} onClick={onClick} />)
    
    await userEvent.click(screen.getByText('Nova'))
    
    expect(onClick).toHaveBeenCalledWith('nova')
  })
})

describe('AgentHireModal', () => {
  it('should show agent selection', () => {
    render(<AgentHireModal isOpen={true} />)
    
    expect(screen.getByText('Hire Agent')).toBeInTheDocument()
    expect(screen.getByText('User Orchestrator')).toBeInTheDocument()
  })
  
  it('should configure agent budget', async () => {
    render(<AgentHireModal isOpen={true} />)
    
    const budgetInput = screen.getByLabelText('Budget (tokens)')
    await userEvent.type(budgetInput, '1000')
    
    expect(budgetInput).toHaveValue(1000)
  })
  
  it('should hire agent', async () => {
    const onHire = vi.fn()
    render(<AgentHireModal isOpen={true} onHire={onHire} />)
    
    // Select agent
    await userEvent.click(screen.getByText('User Orchestrator'))
    
    // Set budget
    const budgetInput = screen.getByLabelText('Budget (tokens)')
    await userEvent.type(budgetInput, '1000')
    
    // Hire
    await userEvent.click(screen.getByText('Hire'))
    
    expect(onHire).toHaveBeenCalledWith({
      agentId: 'user-orchestrator',
      budget: 1000
    })
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// CUSTOM HOOKS TESTS
// ═══════════════════════════════════════════════════════════════════════════

import { useThreads } from '../hooks/useThreads'
import { useSphere } from '../hooks/useSphere'
import { useCache } from '../hooks/useCache'

describe('useThreads hook', () => {
  it('should fetch threads', async () => {
    const { result } = renderHook(() => useThreads('personal'))
    
    // Initially loading
    expect(result.current.loading).toBe(true)
    
    // Wait for data
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
    
    expect(result.current.threads).toBeInstanceOf(Array)
  })
  
  it('should create thread', async () => {
    const { result } = renderHook(() => useThreads('personal'))
    
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
    
    await act(async () => {
      await result.current.createThread({
        title: 'New Thread',
        description: 'Test'
      })
    })
    
    expect(result.current.threads).toContainEqual(
      expect.objectContaining({ title: 'New Thread' })
    )
  })
  
  it('should handle errors', async () => {
    // Mock API error
    global.fetch = vi.fn(() => Promise.reject('API Error'))
    
    const { result } = renderHook(() => useThreads('personal'))
    
    await waitFor(() => {
      expect(result.current.error).toBeTruthy()
    })
  })
})

describe('useSphere hook', () => {
  it('should track active sphere', () => {
    const { result } = renderHook(() => useSphere())
    
    expect(result.current.activeSphere).toBe('personal') // Default
  })
  
  it('should change sphere', () => {
    const { result } = renderHook(() => useSphere())
    
    act(() => {
      result.current.setActiveSphere('business')
    })
    
    expect(result.current.activeSphere).toBe('business')
  })
  
  it('should persist sphere in localStorage', () => {
    const { result } = renderHook(() => useSphere())
    
    act(() => {
      result.current.setActiveSphere('business')
    })
    
    expect(localStorage.getItem('activeSphere')).toBe('business')
  })
})

describe('useCache hook', () => {
  it('should cache data', async () => {
    const { result } = renderHook(() => useCache())
    
    act(() => {
      result.current.set('test-key', { data: 'test' }, 60)
    })
    
    const cached = result.current.get('test-key')
    expect(cached).toEqual({ data: 'test' })
  })
  
  it('should respect TTL', async () => {
    vi.useFakeTimers()
    
    const { result } = renderHook(() => useCache())
    
    act(() => {
      result.current.set('test-key', { data: 'test' }, 1) // 1 second TTL
    })
    
    // Advance time by 2 seconds
    act(() => {
      vi.advanceTimersByTime(2000)
    })
    
    const cached = result.current.get('test-key')
    expect(cached).toBeNull() // Expired
    
    vi.useRealTimers()
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTION TESTS
// ═══════════════════════════════════════════════════════════════════════════

import { formatTimestamp, truncateText, validateEmail } from '../utils/helpers'

describe('Utility Functions', () => {
  describe('formatTimestamp', () => {
    it('should format recent timestamps', () => {
      const now = new Date()
      expect(formatTimestamp(now.toISOString())).toBe('Just now')
      
      const oneMinuteAgo = new Date(now.getTime() - 60000)
      expect(formatTimestamp(oneMinuteAgo.toISOString())).toBe('1 minute ago')
    })
    
    it('should format old timestamps', () => {
      const old = new Date('2024-01-01')
      expect(formatTimestamp(old.toISOString())).toContain('Jan 1')
    })
  })
  
  describe('truncateText', () => {
    it('should truncate long text', () => {
      const long = 'This is a very long text that should be truncated'
      expect(truncateText(long, 20)).toBe('This is a very long...')
    })
    
    it('should not truncate short text', () => {
      const short = 'Short text'
      expect(truncateText(short, 20)).toBe('Short text')
    })
  })
  
  describe('validateEmail', () => {
    it('should validate correct emails', () => {
      expect(validateEmail('test@example.com')).toBe(true)
      expect(validateEmail('user+tag@domain.co.uk')).toBe(true)
    })
    
    it('should reject invalid emails', () => {
      expect(validateEmail('invalid')).toBe(false)
      expect(validateEmail('@example.com')).toBe(false)
      expect(validateEmail('test@')).toBe(false)
    })
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURATION FILES
// ═══════════════════════════════════════════════════════════════════════════

/*
// vitest.config.ts

import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  
  test: {
    // Environment
    environment: 'jsdom',
    
    // Setup files
    setupFiles: ['./tests/setup.ts'],
    
    // Coverage
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.spec.ts',
        '**/*.test.ts'
      ],
      thresholds: {
        lines: 85,
        functions: 85,
        branches: 80,
        statements: 85
      }
    },
    
    // Globals
    globals: true,
    
    // Reporters
    reporters: ['verbose', 'html'],
    
    // Parallel
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false
      }
    }
  }
})
*/

/*
// tests/setup.ts

import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import matchers from '@testing-library/jest-dom/matchers'

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers)

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}

global.localStorage = localStorageMock as any

// Mock fetch
global.fetch = vi.fn()
*/

/*
// package.json

{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "@vitejs/plugin-react": "^4.2.1",
    "@vitest/ui": "^1.0.4",
    "jsdom": "^23.0.1",
    "vitest": "^1.0.4"
  }
}
*/

// ═══════════════════════════════════════════════════════════════════════════
// RUNNING TESTS
// ═══════════════════════════════════════════════════════════════════════════

/*
INSTALLATION:
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom

RUN TESTS:
npm test                          # Watch mode
npm run test:run                  # Run once
npm run test:ui                   # UI mode
npm run test:coverage             # With coverage

WATCH SPECIFIC:
npm test -- src/components/       # Watch components
npm test -- --grep="ThreadList"   # Specific suite
*/

export {}
