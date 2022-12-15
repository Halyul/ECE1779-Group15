import { useEffect } from "react";
import {
  useLocation,
  Navigate,
} from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux'
import { check_auth, renew } from "@/libs/auth";
import { successfulLogout } from '@/reducers/auth'

export default function Protected({ permission, destination, children }) {
  const isLoggedIn = useSelector((state) => state.user.username);
  const role = useSelector((state) => state.user.role)
  const location = useLocation();
  const dispatch = useDispatch()

  useEffect(() => {
    let timer
    const loop = () => {
      check_auth().then((response) => {
        if (!response) {
          renew().then((resp) => {
            if (!resp.status) {
              dispatch(successfulLogout())
            } else {
              dispatch(successfulLogin({
                username: response.username,
                role: response.role,
                accessToken: response.accessToken,
                idToken: response.idToken,
                refreshToken: response.refreshToken,
              }))
              timer = setTimeout(loop, 5000)
            }
          })
        } else {
          timer = setTimeout(loop, 5000)
        }
      });
    }
    loop()
    return () => clearTimeout(timer)
 }, [])

  if (!isLoggedIn) {
    return <Navigate to={destination || "/"} state={{ from: location }} replace />;
  }

  if (permission !== "all" && permission === "admin" && role !== permission) {
    throw new Response("No Permission", {
      status: 403,
      statusText: "HTTP Forbidden",
    });
  }
  return children;
}