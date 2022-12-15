import { useState, useEffect } from "react";
import {
  Navigate,
  useLocation,
  Link,
  useOutletContext,
} from "react-router-dom";
import {
  Button,
  TextField,
  Grid,
} from "@mui/material";
import LoadingButton from '@mui/lab/LoadingButton';
import { useSelector, useDispatch } from 'react-redux'
import { TooltipOnError } from "@/components/tooltip";
import { BasicCard } from "@/components/card";
import { successfulLogin } from '@/reducers/auth'
import { signIn } from '@/libs/auth'

export default function Login() {
  const dispatch = useDispatch()
  const location = useLocation();
  const isLoggedIn = useSelector((state) => state.user.username);
  const from = location.state?.from?.pathname || "/";
  const [bubble, setBubble] = useOutletContext();

  const [username, setUsername] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);

  useEffect(() => {
    if (location.state?.isRegistered) {
      setBubble({
        ...bubble,
        snackbar: {
          open: true,
          message: "You are now registered! Please login."
        }
      })
    }
  }, [location])

  if (isLoggedIn) {
    return <Navigate to={from} state={{ isLoggedIn: true }} replace />
  }

  return (
    <>
      <BasicCard
        title="Login into an Account"
        content={
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TooltipOnError
                open={usernameError}
                handleClose={() => setUsernameError(false)}
                title="No space is allowed."
                body={
                  <TextField
                    id="username"
                    name="username"
                    label="Username"
                    variant="outlined"
                    value={username}
                    fullWidth
                    onChange={(e) => {
                      let value = e.target.value;
                      setUsernameError(value.includes(" "));
                      setUsername(value.replaceAll(" ", ""));
                    }}
                    error={usernameError}
                  />
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TooltipOnError
                open={passwordError}
                handleClose={() => setPasswordError(false)}
                title="No space is allowed."
                body={
                  <TextField
                    id="password"
                    name="password"
                    label="Password"
                    variant="outlined"
                    value={password}
                    type="password"
                    fullWidth
                    onChange={(e) => {
                      let value = e.target.value;
                      setPasswordError(value.includes(" "));
                      setPassword(value.replaceAll(" ", ""));
                    }}
                    error={passwordError}
                  />
                }
              />
            </Grid>
          </Grid>
        }
        actions={
          <>
            <LoadingButton
              size="small"
              loading={loginLoading}
              onClick={(e) => {
                setLoginLoading(true)
                setBubble({
                  ...bubble,
                  snackbar: {
                    open: true,
                    message: "Validing your credentials..."
                  }
                })
                signIn(username, password).then((response) => {
                  setBubble({
                    ...bubble,
                    snackbar: {
                      open: true,
                      message: response.status ? "You are now logged in!" : response.error
                    }
                  })
                  setLoginLoading(false)
                  if (response.status) {
                    dispatch(successfulLogin({
                      username: response.username,
                      role: response.role,
                      accessToken: response.accessToken,
                      idToken: response.idToken,
                      refreshToken: response.refreshToken,
                    }))
                  }
                })
              }}
            >
              Login
            </LoadingButton>
            <Button
              size="small"
              sx={{ marginLeft: "auto" }}
            >
              <Link to="/register" state={{ from: location }}>Register</Link>
            </Button>
          </>
        }
        sx={{
          maxWidth: "480px",
          margin: "0 auto",
        }}
      />
    </>
  );
}

export const LoginRoute = {
  name: "Login",
  path: "login",
};
