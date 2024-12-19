import { useState, useCallback } from 'react';
import { useSWR } from 'swr';
import axios from 'axios';

// トリガーの型定義
interface Trigger {
  id: string;
  name: string;
  condition: string;
  effectId: string;
  isActive: boolean;
  parameters: {
    threshold?: number;
    interval?: number;
    timeWindow?: number;
  };
}

// APIエンドポイント
const TRIGGERS_API_URL = `${process.env.NEXT_PUBLIC_API_URL}/api/triggers`;

/**
 * トリガー関連のカスタムフック
 * トリガーの取得、作成、更新、削除などの機能を提供
 */
export const useTriggers = () => {
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // トリガー一覧の取得
  const { data: triggers, mutate } = useSWR<Trigger[]>(
    TRIGGERS_API_URL,
    async (url) => {
      const response = await axios.get(url);
      return response.data;
    }
  );

  // トリガーの作成
  const createTrigger = useCallback(async (triggerData: Omit<Trigger, 'id'>) => {
    try {
      setIsLoading(true);
      const response = await axios.post(TRIGGERS_API_URL, triggerData);
      await mutate();
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to create trigger'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの更新
  const updateTrigger = useCallback(async (id: string, triggerData: Partial<Trigger>) => {
    try {
      setIsLoading(true);
      const response = await axios.put(`${TRIGGERS_API_URL}/${id}`, triggerData);
      await mutate();
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to update trigger'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの削除
  const deleteTrigger = useCallback(async (id: string) => {
    try {
      setIsLoading(true);
      await axios.delete(`${TRIGGERS_API_URL}/${id}`);
      await mutate();
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete trigger'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの有効/無効切り替え
  const toggleTrigger = useCallback(async (id: string, isActive: boolean) => {
    try {
      setIsLoading(true);
      const response = await axios.patch(`${TRIGGERS_API_URL}/${id}/toggle`, { isActive });
      await mutate();
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to toggle trigger'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  return {
    triggers,
    isLoading,
    error,
    createTrigger,
    updateTrigger,
    deleteTrigger,
    toggleTrigger,
  };
};

export default useTriggers;
const { 
  triggers, 
  createTrigger, 
  updateTrigger, 
  deleteTrigger, 
  toggleTrigger,
  isLoading,
  error 
} = useTriggers();