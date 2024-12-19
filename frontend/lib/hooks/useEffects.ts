import { useState, useEffect } from 'react';
import { useEffectStore } from '@/store/effectStore';
import { fetchEffects } from '@/lib/api/effects';
import type { Effect } from '@/types/Effect';

/**
 * エフェクトの取得と管理を行うカスタムフック
 */
export const useEffects = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const { effects, setEffects, addEffect } = useEffectStore();

  // エフェクト一覧の取得
  const loadEffects = async () => {
    try {
      setLoading(true);
      const data = await fetchEffects();
      setEffects(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch effects'));
    } finally {
      setLoading(false);
    }
  };

  // 新規エフェクトの追加
  const handleAddEffect = async (effect: Effect) => {
    try {
      addEffect(effect);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to add effect'));
    }
  };

  // エフェクトのフィルタリング
  const filterEffectsByType = (type: string) => {
    return effects.filter(effect => effect.type === type);
  };

  // エフェクトの検索
  const searchEffects = (query: string) => {
    return effects.filter(effect => 
      effect.name.toLowerCase().includes(query.toLowerCase())
    );
  };

  // 特定のエフェクトの取得
  const getEffectById = (id: string) => {
    return effects.find(effect => effect.id === id);
  };

  // 初回マウント時にエフェクトを取得
  useEffect(() => {
    loadEffects();
  }, []);

  return {
    effects,
    loading,
    error,
    loadEffects,
    handleAddEffect,
    filterEffectsByType,
    searchEffects,
    getEffectById,
  };
};

/**
 * 単一のエフェクトを管理するカスタムフック
 */
export const useSingleEffect = (effectId: string) => {
  const [effect, setEffect] = useState<Effect | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadEffect = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/effects/${effectId}`);
        const data = await response.json();
        setEffect(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to fetch effect'));
      } finally {
        setLoading(false);
      }
    };

    if (effectId) {
      loadEffect();
    }
  }, [effectId]);

  return { effect, loading, error };
};

export default useEffects;