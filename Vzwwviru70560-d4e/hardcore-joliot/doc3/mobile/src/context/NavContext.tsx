/**
 * CHE·NU™ — Mobile Navigation Context
 * Provides XState machine to all screens
 */

import React, { createContext } from 'react';
import type { StateFrom, EventFrom } from 'xstate';
import type { navMachine } from '../../../shared/machines/navMachine';

type NavState = StateFrom<typeof navMachine>;
type NavSend = (event: EventFrom<typeof navMachine>) => void;

interface NavContextValue {
  state: NavState;
  send: NavSend;
}

export const NavContext = createContext<NavContextValue>({} as NavContextValue);

export function NavContextProvider({
  value,
  children,
}: {
  value: NavContextValue;
  children: React.ReactNode;
}) {
  return <NavContext.Provider value={value}>{children}</NavContext.Provider>;
}
