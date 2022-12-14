import React from 'react';
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route
} from "react-router-dom";
import { StyledEngineProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Root from "@/routes/root";
import ErrorPage from "@/routes/error-page";
import Login, {
  LoginRoute,
  action as loginAction,
} from "@/routes/login";
import Register, {
  RegisterRoute,
  action as registerAction,
} from "@/routes/register";
import Index, {
  IndexRoute
} from "@/routes/index";
import Upload, {
  UploadRoute,
  action as uploadAction,
} from "@/routes/user/upload";
import Image, {
  ImageRoute,
  PublicRoute,
  loader as imageLoader,
} from "@/routes/image";
import Photos, {
  PhotosRoute,
  loader as photosLoader,
} from "@/routes/user/photos";
import Stats, {
  StatsRoute,
  loader as statsLoader,
} from "@/routes/admin/stats";
import Images, {
  ImagesRoute,
  loader as imagesLoader,
} from "@/routes/admin/images";
import Protected from '@/components/protected';
import store, { persistor } from '@/libs/store';
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import '@/App.css';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      path="/"
      element={
        <Root
          title={import.meta.env.VITE_APP_NAME}
          destinations={{
            all: [IndexRoute,],
            user: [
              UploadRoute,
              PhotosRoute,
            ],
            admin: [
              StatsRoute,
              ImagesRoute,
            ]
          }}
        />
      }
      errorElement={<ErrorPage />}
    >
      <Route errorElement={<ErrorPage />}>
        <Route
          path={PublicRoute.path}
          element={
            <Image
              route={PublicRoute.path}
            />
          }
          loader={imageLoader}
        />
        <Route
          path={LoginRoute.path}
          element={<Login />}
          action={loginAction}
        />
        <Route
          path={RegisterRoute.path}
          element={<Register />}
          action={registerAction}
        />
        <Route index element={
          <Protected
            permission="all"
            destination="/login"
          >
            <Index />
          </Protected>
        } />
        <Route
          path={UploadRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Upload />
            </Protected>
          }
          action={uploadAction}
        />
        <Route
          path={ImageRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Image
                route={ImageRoute.path}
              />
            </Protected>
          }
          loader={imageLoader}
        />
        <Route
          path={PhotosRoute.path}
          element={
            <Protected
              permission="user"
            >
              <Photos />
            </Protected>
          }
          loader={photosLoader}
        />
        <Route
          path={StatsRoute.path}
          element={
            <Protected
              permission="admin"
            >
              <Stats />
            </Protected>
          }
          loader={statsLoader}
        />
        <Route
          path={ImagesRoute.path}
          element={
            <Protected
              permission="admin"
            >
              <Images />
            </Protected>
          }
          loader={imagesLoader}
        />
      </Route>
    </Route>
  )
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CssBaseline />
    <StyledEngineProvider injectFirst>
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <RouterProvider router={router} />
        </PersistGate>
      </Provider>
    </StyledEngineProvider>
  </React.StrictMode>
)