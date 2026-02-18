/**
 * Shared TypeScript types for the application.
 */

export interface User {
  userId: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface NavItem {
  name: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
}
