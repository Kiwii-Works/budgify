/**
 * Temporary session management using localStorage.
 * This will be replaced with JWT authentication in Phase 2.
 */

export interface Session {
  userId: string;
  tenantId: string;
  username: string;
  email: string;
}

const SESSION_KEY = 'budgify_session';

export function setSession(session: Session): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
}

export function getSession(): Session | null {
  if (typeof window !== 'undefined') {
    const sessionData = localStorage.getItem(SESSION_KEY);
    if (sessionData) {
      try {
        return JSON.parse(sessionData) as Session;
      } catch {
        return null;
      }
    }
  }
  return null;
}

export function clearSession(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(SESSION_KEY);
  }
}

export function isAuthenticated(): boolean {
  return getSession() !== null;
}
