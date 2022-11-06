import React from 'react';
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";
import { StyledEngineProvider } from '@mui/material/styles';
import Root from "./routes/root";
import ErrorPage from "./routes/error-page";
import Index, {
  IndexRoute
} from "./routes/index";
import Status, {
  StatusRoute,
  loader as statusLoader,
  action as statusAction,
} from "./routes/status";
import Config, {
  ConfigRoute,
  loader as configLoader,
  action as configAction,
} from "./routes/config";
import 'reset-css';
import './App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Root
          title="Manager UI"
          destinations={[
            IndexRoute,
            ConfigRoute,
            StatusRoute,
          ]}
        />
      }
      errorElement={<ErrorPage />}
    >
      <Route errorElement={<ErrorPage />}>
        <Route index element={<Index />} />
        <Route
          path={ConfigRoute.path}
          element={<Config />}
          loader={configLoader}
          action={configAction}
        />
        <Route
          path={StatusRoute.path}
          element={<Status />}
          loader={statusLoader}
          action={statusAction}
        />
      </Route>
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
        <RouterProvider router={router} />
    </StyledEngineProvider>
  </React.StrictMode>
)