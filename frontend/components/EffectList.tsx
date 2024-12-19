'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Pagination, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { useEffectStore } from '@/store/effectStore';
import { fetchEffects } from '@/services/api/effects';
import { Effect } from '@/types/Effect';
import EffectCard from './EffectCard';
import Loading from '../Common/Loading';

const ITEMS_PER_PAGE = 12;

export default function EffectList() {
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [effectType, setEffectType] = useState('all');
  const { effects, setEffects } = useEffectStore();
  const [filteredEffects, setFilteredEffects] = useState<Effect[]>([]);

  useEffect(() => {
    const loadEffects = async () => {
      try {
        const data = await fetchEffects();
        setEffects(data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch effects:', error);
        setLoading(false);
      }
    };
    loadEffects();
  }, [setEffects]);

  useEffect(() => {
    let filtered = [...effects];

    // 検索フィルター
    if (search) {
      filtered = filtered.filter(effect => 
        effect.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    // タイプフィルター
    if (effectType !== 'all') {
      filtered = filtered.filter(effect => effect.type === effectType);
    }

    setFilteredEffects(filtered);
  }, [effects, search, effectType]);

  // ページネーションの計算
  const totalPages = Math.ceil(filteredEffects.length / ITEMS_PER_PAGE);
  const currentPageEffects = filteredEffects.slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  );

  if (loading) return <Loading />;

  return (
    <Box sx={{ p: { xs: 2, md: 4 } }}>
      {/* フィルターコントロール */}
      <Box sx={{ mb: 4, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <TextField
          label="エフェクトを検索"
          variant="outlined"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          sx={{ minWidth: 200 }}
        />
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>エフェクトタイプ</InputLabel>
          <Select
            value={effectType}
            label="エフェクトタイプ"
            onChange={(e) => setEffectType(e.target.value)}
          >
            <MenuItem value="all">すべて</MenuItem>
            <MenuItem value="particle">パーティクル</MenuItem>
            <MenuItem value="sound">サウンド</MenuItem>
            <MenuItem value="visual">ビジュアル</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* エフェクト一覧 */}
      <Grid container spacing={3}>
        {currentPageEffects.map((effect) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={effect.id}>
            <EffectCard effect={effect} />
          </Grid>
        ))}
      </Grid>

      {/* ページネーション */}
      {totalPages > 1 && (
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(_, newPage) => setPage(newPage)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
}