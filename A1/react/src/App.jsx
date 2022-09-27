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
  UploadRoute
} from "./routes/upload";
import Image, {
  ImageRoute,
  ImageWithKeyRoute
} from "./routes/image";
import Keys, {
  KeysRoute
} from "./routes/keys";
import Config, {
  ConfigRoute
} from "./routes/config";
import Status, {
  StatusRoute
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
        />
        <Route
          path={ImageRoute.path}
          element={<Image />}
        />
        <Route
          path={ImageWithKeyRoute.path}
          element={<Image />}
        />
        <Route
          path={KeysRoute.path}
          element={<Keys />}
        />
        <Route
          path={ConfigRoute.path}
          element={<Config />}
        />
        <Route
          path={StatusRoute.path}
          element={<Status />}
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