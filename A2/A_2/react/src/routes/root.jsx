import { Outlet, NavLink, useNavigation } from "react-router-dom";
import React, { useState, useMemo } from "react";
import {
  AppBar,
  Box,
  SwipeableDrawer,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Toolbar,
  Typography,
  Button,
  LinearProgress,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const drawerWidth = 240;

export default function Root(props) {
  const navigation = useNavigation();
  const [isDrawerOpen, setisDrawerOpen] = useState(false);
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light",
        },
      }),
    [prefersDarkMode]
  );

  const handleDrawerToggle = () => {
    setisDrawerOpen(!isDrawerOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          display: "flex",
          minHeight: "inherit",
        }}
      >
        <AppBar component="nav">
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { md: "none" } }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              {props.title}
            </Typography>
            <Box sx={{ display: { xs: "none", md: "block" } }}>
              {props.destinations.map((item) => (
                <Button key={item.name} sx={{ color: "#fff" }}>
                  <NavLink to={item.path}>{item.name}</NavLink>
                </Button>
              ))}
            </Box>
          </Toolbar>
          <Box
            sx={{
              width: "100%",
            }}
            hidden={navigation.state !== "loading"}
          >
            <LinearProgress />
          </Box>
        </AppBar>
        <Box component="nav">
          <SwipeableDrawer
            container={document.body}
            variant="temporary"
            open={isDrawerOpen}
            onClose={handleDrawerToggle}
            onOpen={handleDrawerToggle}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
            sx={{
              display: { md: "none" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: drawerWidth,
              },
            }}
          >
            <Box onClick={handleDrawerToggle} sx={{ textAlign: "center" }}>
              <List>
                {props.destinations.map((item) => (
                  <NavLink to={item.path} key={item.name}>
                    <ListItem disablePadding>
                      <ListItemButton sx={{ textAlign: "center" }}>
                        <ListItemText primary={item.name} />
                      </ListItemButton>
                    </ListItem>
                  </NavLink>
                ))}
              </List>
            </Box>
          </SwipeableDrawer>
        </Box>
        <Box
          component="main"
          sx={{
            height: "inherit",
            width: "90vw",
            maxWidth: "768px !important",
            margin: "0 auto",
          }}
        >
          <Toolbar sx={{ marginBottom: "16px" }} />
          <Outlet />
        </Box>
      </Box>
    </ThemeProvider>
  );
}
