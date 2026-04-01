function getStoredUserInfo() {
  const raw = sessionStorage.getItem('user-info');
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch (err) {
    sessionStorage.removeItem('user-info');
    return null;
  }
}

export function isAuthenticated() {
  const userInfo = getStoredUserInfo();
  const token = userInfo?.access_token;

  if (!token) {
    return false;
  }

  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      return false;
    }

    const payload = JSON.parse(atob(parts[1]));
    const now = Math.floor(Date.now() / 1000);

    if (payload.exp && payload.exp < now) {
      sessionStorage.removeItem('user-info');
      return false;
    }

    return true;
  } catch (err) {
    console.error('Invalid token format:', err);
    sessionStorage.removeItem('user-info');
    return false;
  }
}
