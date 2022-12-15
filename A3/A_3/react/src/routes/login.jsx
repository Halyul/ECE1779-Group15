import { useState, useEffect } from "react";
import {
  Navigate,
  useLocation,
  useActionData,
  Link,
} from "react-router-dom";
import {
  Button,
  TextField,
  Grid,
  Snackbar,
} from "@mui/material";
import { useSelector, useDispatch } from 'react-redux'
import { TooltipOnError } from "@/components/tooltip";
import { FormCard } from "@/components/card";
import SubmissionPrompt from "@/components/submission-prompt";
import { login } from '@/reducers/auth'

export async function action({ request, params }) {
  console.log(123)
  return redirect("/login?register=true");
}

export default function Login() {
  const dispatch = useDispatch()
  const location = useLocation();
  const actionResponse = useActionData();
  const token = useSelector((state) => state.user.token);
  const [isRegistered, setIsRegistered] = useState(location.state?.isRegistered);
  const from = location.state?.from?.pathname || "/";

  const [submitted, setSubmitted] = useState(false);
  const [username, setUsername] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState(false);

  const handleSnackbarClose = () => {
    setIsRegistered(false);
  };
  
  if (token) {
    return <Navigate to={from} replace />
  }

  return (
    <>
      <FormCard
        id="login"
        method="POST"
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
            <Button
              size="small"
              type="submit"
              onClick={(e) => {
                dispatch(login({
                  username: username,
                  password: password,
                }))
              }}
            >
              Login
            </Button>
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
      <SubmissionPrompt
        failed={{
          title: "Failed to commit changes",
          text: actionResponse?.statusText,
        }}
        submitting={{
          text: "Commiting changes...",
          open: submitted,
          setOpen: setSubmitted,
        }}
        submittedText="Changes committed successfully"
        submissionStatus={actionResponse}
      />
      <Snackbar
        open={isRegistered}
        message="You are now registered! Please login."
        onClose={handleSnackbarClose}
      />
    </>
  );
}

export const LoginRoute = {
  name: "Login",
  path: "login",
};
