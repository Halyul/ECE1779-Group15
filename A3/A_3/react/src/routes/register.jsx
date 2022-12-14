import { useState, useEffect } from "react";
import {
  Navigate,
  useLocation,
  useActionData,
  Link,
  redirect
} from "react-router-dom";
import {
  Box,
  Button,
  TextField,
  Grid,
} from "@mui/material";
import { useSelector, useDispatch } from 'react-redux'
import { TooltipOnError } from "@/components/tooltip";
import { BasicCard } from "@/components/card";
import SubmissionPrompt from "@/components/submission-prompt";
import {
  signUp,
  confirmSignUp,
  resendConfirmationCode,
} from "@/libs/auth";

export async function action({ request, params }) {
  const formData = await request.formData();
  const updates = Object.fromEntries(formData);
  await signUp(updates.username, updates.password, updates.email);
  // return redirect("/login?register=true");
}

export default function Register() {
  const actionResponse = useActionData();
  const token = useSelector((state) => state.user.token)
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";

  const [submitted, setSubmitted] = useState(false);
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState(false);
  const [username, setUsername] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [password2, setPassword2] = useState("");
  const [password2Error, setPassword2Error] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(true);
  const [verificationCode, setVerificationCode] = useState("");
  const [verificationCodeError, setVerificationCodeError] = useState(false);

  if (token) {
    return <Navigate to={from} replace />
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
                    disabled={password === "" && password2 === ""}
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
                  <Button

                  >
                    Resend
                  </Button>
                </Grid>
              </>
            )}
          </Grid>
        }
        actions={
          <>
            {showConfirmation ? (
              <Button
                size="small"
                onClick={() => confirmSignUp("test", "862744")}
              >
                Confirm
              </Button>
            ) : (
              <Button
                size="small"
              >
                Register
              </Button>
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
    </>
  );
}

export const RegisterRoute = {
  name: "Register",
  path: "register",
};
