import { useState } from "react";
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
import { useSelector } from 'react-redux'
import { TooltipOnError } from "@/components/tooltip";
import { BasicCard } from "@/components/card";
import {
  signUp,
  confirmSignUp,
  resendConfirmationCode,
} from "@/libs/auth";

export default function Register() {
  const isLoggedIn = useSelector((state) => state.user.username);
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";

  const [bubble, setBubble] = useOutletContext();

  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState(false);
  const [username, setUsername] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [password2, setPassword2] = useState("");
  const [password2Error, setPassword2Error] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [verificationCode, setVerificationCode] = useState("");
  const [verificationCodeError, setVerificationCodeError] = useState(false);
  const [registered, setRegistered] = useState(false);

  const [registerLoading, setRegisterLoading] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);

  if (isLoggedIn) {
    return <Navigate to={from} replace />
  }

  if (registered) {
    return <Navigate to="/login" replace state={{ isRegistered: true }} />
  }

  return (
    <>
      <BasicCard
        id="register"
        method="POST"
        title="Register an Account"
        content={
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TooltipOnError
                open={emailError}
                handleClose={() => setEmailError(false)}
                title="No space is allowed."
                body={
                  <TextField
                    id="email"
                    name="email"
                    label="Email"
                    variant="outlined"
                    type="email"
                    value={email}
                    fullWidth
                    onChange={(e) => {
                      let value = e.target.value;
                      setEmailError(value.includes(" "));
                      setEmail(value.replaceAll(" ", ""));
                    }}
                    error={emailError}
                  />
                }
              />
            </Grid>
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
                handleClose={() => setPassword2Error(password !== password2)}
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
                      if (password2) {
                        setPassword2Error(value !== password2);
                      }
                    }}
                    error={passwordError}
                  />
                }
              />
            </Grid>
            <Grid item xs={12}>
              <TooltipOnError
                open={password2Error}
                handleClose={() => setPassword2Error(password !== password2)}
                title="Password does not match."
                body={
                  <TextField
                    id="password2"
                    name="password2"
                    label="Re-enter Password"
                    variant="outlined"
                    value={password2}
                    type="password"
                    disabled={(password === "" && password2 === "")}
                    fullWidth
                    onChange={(e) => {
                      let value = e.target.value;
                      setPassword2Error(value !== password);
                      setPassword2(value.replaceAll(" ", ""));
                    }}
                    error={password2Error}
                  />
                }
              />
            </Grid>
            {showConfirmation && (
              <>
                <Grid item xs={10}>
                  <TooltipOnError
                    open={verificationCodeError}
                    handleClose={() => setVerificationCodeError(false)}
                    title="Maximum length is 6 and only numbers are allowed."
                    body={
                      <TextField
                        id="verification_code"
                        name="verification_code"
                        label="Verification Code"
                        variant="outlined"
                        value={verificationCode}
                        fullWidth
                        onChange={(e) => {
                          try {
                            const value = parseInt(e.target.value);
                            setVerificationCode(value < 0 ? "" : (
                              isNaN(value) ? "" : (value >= Math.pow(10, 6) ? verificationCode : value)
                            ));
                            if (value >= 0 && value <= Math.pow(10, 6)) {
                              setVerificationCodeError(false);
                            } else {
                              setVerificationCodeError(true);
                            }
                          } catch {
                            setVerificationCode(0);
                            setVerificationCodeError(true);
                          }
                        }}
                        error={verificationCodeError}
                      />
                    }
                  />
                </Grid>
                <Grid item xs={2} sx={{ display: "flex" }}>
                  <LoadingButton
                    loading={resendLoading}
                    onClick={() => {
                      setResendLoading(true);
                      resendConfirmationCode(username).then((response) => {
                        setBubble({...bubble, snackbarOpen: true, snackbarMessage: response.status ? "Verification code sent!" : response.error});
                        setResendLoading(false);
                      })
                    }}
                  >
                    Resend
                  </LoadingButton>
                </Grid>
              </>
            )}
          </Grid>
        }
        actions={
          <>
            {showConfirmation ? (
              <LoadingButton
                size="small"
                loading={confirmLoading}
                onClick={() => {
                  setConfirmLoading(true);
                  confirmSignUp(username, verificationCode).then((response) => {
                    setBubble({...bubble, snackbarOpen: true, snackbarMessage: response.status ? "Registered successfully!" : response.error});
                    setRegistered(response.status);
                    setConfirmLoading(false);
                  })
                }}
              >
                Confirm
              </LoadingButton>
            ) : (
              <LoadingButton
                  size="small"
                  loading={registerLoading}
                  onClick={() => {
                    setRegisterLoading(true);
                    setBubble({...bubble, snackbarOpen: true, snackbarMessage: "Registering..."})
                    signUp(username, password, email).then((response) => {
                      setBubble({...bubble, snackbarOpen: true, snackbarMessage: response.status ? "Please check your mailbox for verification code!" : response.error});
                      setShowConfirmation(response.status);
                      setRegisterLoading(false);
                    })
                  }}
              >
                Register
              </LoadingButton>
            )}
            <Button
              size="small"
              sx={{ marginLeft: "auto" }}
            >
              <Link to={from}>Back</Link>
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

export const RegisterRoute = {
  name: "Register",
  path: "register",
};
