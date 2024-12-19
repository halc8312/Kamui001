import axios from 'axios';
import { Effect } from '../types/Effect';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * エフェクト関連のAPI呼び出し関数をまとめたモジュール
 */

/**
 * 全てのエフェクトを取得する
 * @returns Promise<Effect[]>
 */
export const fetchEffects = async (): Promise<Effect[]> => {
  try {
    const response = await axios.get<Effect[]>(`${API_BASE_URL}/api/magic_effects`);
    return response.data;
  } catch (error) {
    console.error('Error fetching effects:', error);
    throw error;
  }
};

/**
 * 特定のエフェクトを取得する
 * @param id エフェクトID
 * @returns Promise<Effect>
 */
export const fetchEffectById = async (id: string): Promise<Effect> => {
  try {
    const response = await axios.get<Effect>(`${API_BASE_URL}/api/magic_effects/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching effect with id ${id}:`, error);
    throw error;
  }
};

/**
 * 新しいエフェクトを作成する
 * @param effect 作成するエフェクトのデータ
 * @returns Promise<Effect>
 */
export const createEffect = async (effect: Omit<Effect, 'id'>): Promise<Effect> => {
  try {
    const response = await axios.post<Effect>(`${API_BASE_URL}/api/magic_effects`, effect);
    return response.data;
  } catch (error) {
    console.error('Error creating effect:', error);
    throw error;
  }
};

/**
 * エフェクトを更新する
 * @param id エフェクトID
 * @param effect 更新するエフェクトのデータ
 * @returns Promise<Effect>
 */
export const updateEffect = async (id: string, effect: Partial<Effect>): Promise<Effect> => {
  try {
    const response = await axios.put<Effect>(`${API_BASE_URL}/api/magic_effects/${id}`, effect);
    return response.data;
  } catch (error) {
    console.error(`Error updating effect with id ${id}:`, error);
    throw error;
  }
};

/**
 * エフェクトを削除する
 * @param id エフェクトID
 * @returns Promise<void>
 */
export const deleteEffect = async (id: string): Promise<void> => {
  try {
    await axios.delete(`${API_BASE_URL}/api/magic_effects/${id}`);
  } catch (error) {
    console.error(`Error deleting effect with id ${id}:`, error);
    throw error;
  }
};

/**
 * エフェクトを適用する
 * @param id エフェクトID
 * @param parameters 適用するパラメータ
 * @returns Promise<void>
 */
export const applyEffect = async (
  id: string, 
  parameters: { color: string; duration: number; intensity: number }
): Promise<void> => {
  try {
    await axios.post(`${API_BASE_URL}/api/magic_effects/${id}/apply`, parameters);
  } catch (error) {
    console.error(`Error applying effect with id ${id}:`, error);
    throw error;
  }
};