import {
  Outlet,
  Link,
  NavLink,
  useNavigation,
  useLocation,
  useNavigate
} from "react-router-dom";
import React, { useState, useMemo } from "react";
import {
  useSelector,
  useDispatch
} from 'react-redux'
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
  SpeedDial,
  SpeedDialAction
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { logout } from '@/reducers/auth'

const drawerWidth = 240;

export default function Root(props) {
  const navigation = useNavigation();
  const navigate = useNavigate();
  const dispatch = useDispatch()
  const location = useLocation();
  const token = useSelector((state) => state.user.token)
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

  const fabActions = [
    { icon: <ArrowBackIcon />, name: "Back", onClick: () => navigate(-1) },
    { icon: <ArrowForwardIcon />, name: "Forward", onClick: () => navigate(1) },
  ];

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
            {token && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2, display: { md: "none" } }}
              >
                <MenuIcon />
              </IconButton>
            )}
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              <Link to="/">{props.title}</Link>
            </Typography>
            {!token && location.pathname !== "/login" && (
              <Button
                color="inherit"
              >
                <Link to="/login">Login</Link>
              </Button>
            )}
            {token && (
              <>
                <Box sx={{ display: { xs: "none", md: "block" } }}>
                  {props.destinations.map((item) => (

                    <NavLink to={item.path} key={item.name}>
                    {({ isActive }) => (
                        <Button
                          color={isActive ? "secondary" : "inherit"}
                        >
                        {item.name}
                      </Button>
                    )}
                    </NavLink>
                  ))}
                </Box>
                <Button
                  color="inherit"
                  onClick={() => dispatch(logout())}
                >
                  Logout
                </Button>
              </>
            )}
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
        {token && (
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
                      {({ isActive }) => (
                        <ListItemButton
                          selected={isActive}
                          sx={{ textAlign: "center" }}>
                          <ListItemText primary={item.name} />
                        </ListItemButton>
                      )}
                    </NavLink>
                  ))}
                </List>
              </Box>
            </SwipeableDrawer>
          </Box>
        )}
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
        <SpeedDial
          ariaLabel="SpeedDial playground example"
          icon={<SpeedDialIcon />}
          direction="up"
          sx={{ position: "absolute", bottom: 32, right: 32 }}
        >
          {fabActions.map((action) => (
            <SpeedDialAction
              key={action.name}
              icon={action.icon}
              tooltipTitle={action.name}
              onClick={action.onClick}
            />
          ))}
        </SpeedDial>
      </Box>
    </ThemeProvider>
  );
}
