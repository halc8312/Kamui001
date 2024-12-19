'use client';

import { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Grid, CircularProgress } from '@mui/material';
import useSWR from 'swr';
import axios from 'axios';

// トリガーのインターフェース定義
interface Trigger {
  id: string;
  name: string;
  condition: {
    type: string;
    value: any;
  };
  active: boolean;
  created_at: string;
  updated_at: string;
}

// トリガーフェッチャー関数
const fetchTriggers = async () => {
  const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/triggers`);
  return response.data;
};

export default function TriggerList() {
  // SWRを使用したデータフェッチング
  const { data: triggers, error, mutate } = useSWR<Trigger[]>('/api/triggers', fetchTriggers, {
    refreshInterval: 30000, // 30秒ごとに更新
  });

  // ローディング状態の処理
  if (!triggers && !error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  // エラー状態の処理
  if (error) {
    return (
      <Box p={3}>
        <Typography color="error">
          トリガーの読み込み中にエラーが発生しました。
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', p: { xs: 2, md: 3 } }}>
      <Typography variant="h5" component="h2" gutterBottom>
        トリガー一覧
      </Typography>
      
      <Grid container spacing={3}>
        {triggers?.map((trigger) => (
          <Grid item xs={12} sm={6} md={4} key={trigger.id}>
            <Card 
              sx={{ 
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                }
              }}
            >
              <CardContent>
                <Typography variant="h6" component="h3" gutterBottom>
                  {trigger.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  条件タイプ: {trigger.condition.type}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  条件値: {JSON.stringify(trigger.condition.value)}
                </Typography>
                <Typography 
                  variant="body2" 
                  color={trigger.active ? "success.main" : "error.main"}
                  sx={{ mt: 1 }}
                >
                  ステータス: {trigger.active ? "有効" : "無効"}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {triggers?.length === 0 && (
        <Box textAlign="center" py={4}>
          <Typography color="text.secondary">
            トリガーが設定されていません
          </Typography>
        </Box>
      )}
    </Box>
  );
}

// パフォーマンス最適化のためのメモ化
export const MemoizedTriggerList = React.memo(TriggerList);