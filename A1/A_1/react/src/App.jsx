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
import Upload, {
  UploadRoute,
  action as uploadAction,
} from "./routes/upload";
import Image, {
  ImageRoute,
  ImageWithKeyRoute,
  loader as imageLoader,
  action as imageAction,
} from "./routes/image";
import Keys, {
  KeysRoute,
  loader as keysLoader,
  action as keysAction,
} from "./routes/keys";
import Config, {
  ConfigRoute,
  loader as configLoader,
  action as configAction,
} from "./routes/config";
import Status, {
  StatusRoute,
  loader as statusLoader,
  action as statusAction,
} from "./routes/status";
import 'reset-css';
import './App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Root
          title="ECE1779 Group 15"
          destinations={[
            IndexRoute,
            UploadRoute,
            ImageRoute,
            KeysRoute,
            ConfigRoute,
            StatusRoute
          ]}
        />
      }
      errorElement={<ErrorPage />}
    >
      <Route errorElement={<ErrorPage />}>
        <Route index element={<Index />} />
        <Route
          path={UploadRoute.path}
          element={<Upload />}
          action={uploadAction}
        />
        <Route
          path={ImageRoute.path}
          element={<Image />}
          action={imageAction}
        />
        <Route
          path={ImageWithKeyRoute.path}
          element={<Image />}
          loader={imageLoader}
          action={imageAction}
        />
        <Route
          path={KeysRoute.path}
          element={<Keys />}
          loader={keysLoader}
          action={keysAction}
        />
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