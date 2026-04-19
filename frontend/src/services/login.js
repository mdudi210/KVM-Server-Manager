import { apiClient } from '@/config/api';

export async function login(username, password) {
  const response = await apiClient.post('/login', {
    username,
    password,
  });

  return response;
}
