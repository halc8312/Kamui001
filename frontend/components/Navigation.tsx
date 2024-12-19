'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { 
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  Box, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Effects as EffectsIcon,
  Home as HomeIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

// スタイル付きコンポーネントの定義
const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  boxShadow: 'none',
  borderBottom: `1px solid ${theme.palette.divider}`,
}));

const StyledLink = styled(Link)(({ theme }) => ({
  textDecoration: 'none',
  color: theme.palette.text.primary,
  '&:hover': {
    color: theme.palette.primary.main,
  },
}));

// ナビゲーションアイテムの定義
const navItems = [
  { title: 'Home', path: '/', icon: HomeIcon },
  { title: 'Dashboard', path: '/dashboard', icon: DashboardIcon },
  { title: 'Effects', path: '/effects', icon: EffectsIcon },
];

const Navigation = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const pathname = usePathname();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // ドロワーの内容
  const drawer = (
    <Box
      onClick={handleDrawerToggle}
      sx={{ textAlign: 'center' }}
      role="presentation"
    >
      <IconButton
        sx={{ position: 'absolute', right: 8, top: 8 }}
        onClick={handleDrawerToggle}
      >
        <CloseIcon />
      </IconButton>
      <Typography variant="h6" sx={{ my: 2 }}>
        StockSense
      </Typography>
      <List>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <ListItem key={item.path}>
              <StyledLink href={item.path}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <ListItemIcon>
                    <Icon />
                  </ListItemIcon>
                  <ListItemText primary={item.title} />
                </Box>
              </StyledLink>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  return (
    <>
      <StyledAppBar position="fixed">
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, color: theme.palette.text.primary }}
          >
            StockSense
          </Typography>
          {!isMobile && (
            <Box sx={{ display: 'flex', gap: 2 }}>
              {navItems.map((item) => (
                <StyledLink
                  key={item.path}
                  href={item.path}
                  sx={{
                    fontWeight: pathname === item.path ? 'bold' : 'normal',
                    borderBottom: pathname === item.path ? 
                      `2px solid ${theme.palette.primary.main}` : 'none',
                  }}
                >
                  {item.title}
                </StyledLink>
              ))}
            </Box>
          )}
        </Toolbar>
      </StyledAppBar>

      {/* モバイルナビゲーションドロワー */}
      <Drawer
        variant="temporary"
        anchor="left"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better mobile performance
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
        }}
      >
        {drawer}
      </Drawer>
      
      {/* ツールバーの高さ分のスペーサー */}
      <Toolbar />
    </>
  );
};

export default Navigation;