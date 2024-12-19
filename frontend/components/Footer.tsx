'use client';

import React from 'react';
import { Box, Container, Grid, Typography, Link, useTheme, useMediaQuery } from '@mui/material';
import { styled } from '@mui/material/styles';

// スタイル付きコンポーネントの定義
const FooterWrapper = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(6, 0),
  marginTop: 'auto',
}));

const FooterLink = styled(Link)(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  textDecoration: 'none',
  '&:hover': {
    textDecoration: 'underline',
  },
}));

const Footer = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const footerSections = [
    {
      title: 'About',
      links: [
        { text: 'About Us', href: '/about' },
        { text: 'Contact', href: '/contact' },
        { text: 'Privacy Policy', href: '/privacy' },
      ],
    },
    {
      title: 'Services',
      links: [
        { text: 'Effects Library', href: '/effects' },
        { text: 'Dashboard', href: '/dashboard' },
        { text: 'API Documentation', href: '/docs' },
      ],
    },
    {
      title: 'Connect',
      links: [
        { text: 'Twitter', href: 'https://twitter.com/stocksense' },
        { text: 'GitHub', href: 'https://github.com/stocksense' },
        { text: 'Discord', href: 'https://discord.gg/stocksense' },
      ],
    },
  ];

  const currentYear = new Date().getFullYear();

  return (
    <FooterWrapper component="footer">
      <Container maxWidth="lg">
        <Grid container spacing={4} justifyContent="space-between">
          {footerSections.map((section, index) => (
            <Grid item xs={12} sm={4} key={index}>
              <Typography variant={isMobile ? 'h6' : 'h5'} gutterBottom>
                {section.title}
              </Typography>
              <Box component="nav" aria-label={`${section.title} navigation`}>
                {section.links.map((link, linkIndex) => (
                  <Box key={linkIndex} mb={1}>
                    <FooterLink
                      href={link.href}
                      target={link.href.startsWith('http') ? '_blank' : '_self'}
                      rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                    >
                      {link.text}
                    </FooterLink>
                  </Box>
                ))}
              </Box>
            </Grid>
          ))}
        </Grid>

        <Box mt={4} pt={4} borderTop={1} borderColor="rgba(255, 255, 255, 0.1)">
          <Typography variant="body2" align="center">
            © {currentYear} StockSense. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </FooterWrapper>
  );
};

export default Footer;