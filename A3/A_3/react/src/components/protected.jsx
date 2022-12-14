import {
  useLocation,
  Navigate,
} from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux'

export default function Protected({ permission, destination, children }) {
  const token = useSelector((state) => state.user.token)
  const role = useSelector((state) => state.user.role)
  const location = useLocation();

  if (!token) {
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