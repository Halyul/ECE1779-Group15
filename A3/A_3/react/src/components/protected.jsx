import {
  useLocation,
  Navigate,
} from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux'

export default function Protected({ permission, children }) {
  const token = useSelector((state) => state.user.token)
  const location = useLocation();
  console.log(permission)
  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}