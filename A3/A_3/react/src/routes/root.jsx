import {
  Outlet,
  Link,
  NavLink,
  useNavigation,
  useLocation,
  useNavigate,
  Navigate
} from "react-router-dom";
import React, { useState, useMemo } from "react";
import {
  useSelector,
  useDispatch
} from 'react-redux'
import {
  AppBar,
  Box,
  Divider,
  Collapse,
  SwipeableDrawer,
  IconButton,
  List,
  ListItemText,
  ListItemButton,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  LinearProgress,
  SpeedDial,
  SpeedDialAction
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { signOut } from '@/libs/auth'
import { successfulLogout } from '@/reducers/auth'

const drawerWidth = 240;

export default function Root(props) {
  const navigation = useNavigation();
  const navigate = useNavigate();
  const dispatch = useDispatch()
  const location = useLocation();
  const isLoggedIn = useSelector((state) => state.user.username);
  const role = useSelector((state) => state.user.role);
  const [isDrawerOpen, setisDrawerOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);
  const [adminMenuAnchorEl, setAdminMenuAnchor] = useState(null);
  const adminMenuOpen = Boolean(adminMenuAnchorEl);
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const [mainCSS, setMainCSS] = useState({
    height: "inherit",
    width: "90vw",
    margin: "0 auto",
  })

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

  const handleAdminMenuOpen = (event) => {
    setAdminMenuAnchor(event.currentTarget);
  };

  const handleAdminMenuClose = () => {
    setAdminMenuAnchor(null);
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
        <AppBar component="nav" position="fixed">

          <Toolbar>
            {isLoggedIn && (
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
            {!isLoggedIn && location.pathname !== "/login" && (
              <Button
                color="inherit"
              >
                <Link to="/login">Login</Link>
              </Button>
            )}
            {isLoggedIn && (
              <>
                <Box sx={{ display: { xs: "none", md: "block" } }}>
                  {[...props.destinations.all, ...props.destinations.user].map((item) => (
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
                  {role === "admin" && (
                    <>
                      <Button
                        aria-controls={adminMenuOpen ? 'admin-menu' : undefined}
                        aria-haspopup="true"
                        aria-expanded={adminMenuOpen ? 'true' : undefined}
                        color="inherit"
                        onClick={handleAdminMenuOpen}
                        endIcon={<KeyboardArrowDownIcon />}
                      >
                        Admin
                      </Button>
                      <Menu
                        id="admin-menu"
                        anchorEl={adminMenuAnchorEl}
                        open={adminMenuOpen}
                        onClose={handleAdminMenuClose}
                        MenuListProps={{
                          "aria-labelledby": "basic-button",
                        }}
                        anchorOrigin={{
                          vertical: "top",
                          horizontal: "right",
                        }}
                        transformOrigin={{
                          vertical: "top",
                          horizontal: "right",
                        }}
                      >
                        <Box>
                          {props.destinations.admin.map((item) => (
                            <NavLink to={item.path} key={item.name}>
                              {({ isActive }) => (
                                <MenuItem
                                  selected={isActive}
                                  onClick={() => {
                                    handleAdminMenuClose();
                                  }}
                                >
                                  {item.name}
                                </MenuItem>
                              )}
                            </NavLink>
                          ))}
                        </Box>
                        <Divider sx={{ my: 0.5 }} />
                        <MenuItem onClick={handleAdminMenuClose}>
                          Close
                        </MenuItem>
                      </Menu>
                    </>
                  )}
                </Box>
                <Button
                  color="inherit"
                  onClick={() => {
                    signOut().then((resp) => {
                      dispatch(successfulLogout());
                    })
                  }}
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
        {isLoggedIn && (
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
              <Box>
                <List>
                  {[...props.destinations.all, ...props.destinations.user].map((item) => (
                    <NavLink to={item.path} key={item.name}>
                      {({ isActive }) => (
                        <ListItemButton
                          selected={isActive}
                          onClick={handleDrawerToggle}
                        >
                          <ListItemText primary={item.name} />
                        </ListItemButton>
                      )}
                    </NavLink>
                  ))}
                  {role === "admin" && (
                    <>
                      <ListItemButton onClick={() => setAdminOpen(!adminOpen)}>
                        <ListItemText primary="Admin" />
                        {adminOpen ? <ExpandLess /> : <ExpandMore />}
                      </ListItemButton>
                      <Collapse in={adminOpen} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding>
                          {props.destinations[role].map((item) => (
                            <NavLink to={item.path} key={item.name}>
                              {({ isActive }) => (
                                <ListItemButton
                                  selected={isActive}
                                  onClick={handleDrawerToggle}
                                >
                                  <ListItemText primary={item.name} />
                                </ListItemButton>
                              )}
                            </NavLink>
                          ))}
                        </List>
                      </Collapse>
                    </>
                  )}
                </List>
              </Box>
            </SwipeableDrawer>
          </Box>
        )}
        <Box
          component="main"
          sx={mainCSS}
        >
          <Toolbar sx={{ marginBottom: "16px" }} />
          <Outlet context={[mainCSS, setMainCSS]} />
        </Box>
        <SpeedDial
          ariaLabel="SpeedDial playground example"
          icon={<SpeedDialIcon />}
          direction="up"
          sx={{ position: "fixed", bottom: 32, right: 32 }}
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
