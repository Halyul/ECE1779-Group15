import {
  Navigate,
  useLocation
} from "react-router-dom";
import {
  Button,
} from "@mui/material";
import { useSelector, useDispatch } from 'react-redux'
import { login } from '@/reducers/auth'

export default function Login() {
  const dispatch = useDispatch()
  const location = useLocation();
  const token = useSelector((state) => state.user.token)
  const from = location.state?.from?.pathname || "/";

  if (token) {
    return <Navigate to={from} replace />
  }

  return (
    <>
      <Button
        color="inherit"
        onClick={() => dispatch(login({
          username: "test",
          password: "test",
        }))}
      >
        Login
      </Button>
    </>
  );
}

export const LoginRoute = {
  name: "Login",
  path: "login",
};
