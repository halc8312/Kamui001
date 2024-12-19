import axios from 'axios';

// APIのベースURL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// トリガーの型定義
export interface Trigger {
  id: string;
  name: string;
  type: string;
  conditions: {
    threshold: number;
    operator: string;
    target: string;
  };
  effect_id: string;
  active: boolean;
}

// トリガー作成のためのデータ型
export interface CreateTriggerData {
  name: string;
  type: string;
  conditions: {
    threshold: number;
    operator: string;
    target: string;
  };
  effect_id: string;
}

/**
 * すべてのトリガーを取得
 * @returns Promise<Trigger[]>
 */
export const fetchTriggers = async (): Promise<Trigger[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/triggers`);
    return response.data;
  } catch (error) {
    console.error('Error fetching triggers:', error);
    throw error;
  }
};

/**
 * 特定のトリガーを取得
 * @param id トリガーID
 * @returns Promise<Trigger>
 */
export const fetchTriggerById = async (id: string): Promise<Trigger> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/triggers/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching trigger ${id}:`, error);
    throw error;
  }
};

/**
 * 新しいトリガーを作成
 * @param data 作成するトリガーのデータ
 * @returns Promise<Trigger>
 */
export const createTrigger = async (data: CreateTriggerData): Promise<Trigger> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/triggers`, data);
    return response.data;
  } catch (error) {
    console.error('Error creating trigger:', error);
    throw error;
  }
};

/**
 * トリガーを更新
 * @param id トリガーID
 * @param data 更新するデータ
 * @returns Promise<Trigger>
 */
export const updateTrigger = async (
  id: string,
  data: Partial<CreateTriggerData>
): Promise<Trigger> => {
  try {
    const response = await axios.put(`${API_BASE_URL}/api/triggers/${id}`, data);
    return response.data;
  } catch (error) {
    console.error(`Error updating trigger ${id}:`, error);
    throw error;
  }
};

/**
 * トリガーを削除
 * @param id トリガーID
 * @returns Promise<void>
 */
export const deleteTrigger = async (id: string): Promise<void> => {
  try {
    await axios.delete(`${API_BASE_URL}/api/triggers/${id}`);
  } catch (error) {
    console.error(`Error deleting trigger ${id}:`, error);
    throw error;
  }
};

/**
 * トリガーの有効/無効を切り替え
 * @param id トリガーID
 * @param active 有効にするかどうか
 * @returns Promise<Trigger>
 */
export const toggleTriggerActive = async (
  id: string,
  active: boolean
): Promise<Trigger> => {
  try {
    const response = await axios.patch(`${API_BASE_URL}/api/triggers/${id}/toggle`, {
      active,
    });
    return response.data;
  } catch (error) {
    console.error(`Error toggling trigger ${id}:`, error);
    throw error;
  }
};