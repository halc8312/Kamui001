import axios from 'axios';

// 環境変数からAPIのベースURLを取得
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  username: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    username: string;
  };
}

/**
 * ログイン認証を行う
 * @param credentials ログイン情報（メールアドレスとパスワード）
 * @returns 認証レスポンス
 */
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
};

/**
 * ユーザー登録を行う
 * @param userData 登録するユーザー情報
 * @returns 認証レスポンス
 */
export const register = async (userData: RegisterData): Promise<AuthResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
};

/**
 * ログアウト処理を行う
 */
export const logout = async (): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`,
      },
    });
    // ローカルストレージからトークンを削除
    localStorage.removeItem('access_token');
  } catch (error) {
    throw handleAuthError(error);
  }
};

/**
 * 現在のユーザー情報を取得する
 * @returns ユーザー情報
 */
export const getCurrentUser = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`,
      },
    });
    return response.data;
  } catch (error) {
    throw handleAuthError(error);
  }
};

/**
 * アクセストークンを取得する
 * @returns アクセストークン
 */
export const getAccessToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
};

/**
 * 認証エラーをハンドリングする
 * @param error エラーオブジェクト
 * @returns 整形されたエラー
 */
const handleAuthError = (error: any) => {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.message || 'Authentication failed';
    return new Error(message);
  }
  return error;
};

/**
 * リクエストインターセプターをセットアップする
 */
axios.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * レスポンスインターセプターをセットアップする
 */
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // トークンが無効な場合の処理
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);