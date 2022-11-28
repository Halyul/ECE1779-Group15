import {
    configureStore,
    combineReducers
} from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import storage from 'redux-persist/lib/storage'
import {
    persistReducer,
    persistStore,
    FLUSH,
    REHYDRATE,
    PAUSE,
    PERSIST,
    PURGE,
    REGISTER,
} from 'redux-persist'
import userReducer from '@/reducers/auth'

const persistConfig = {
    key: "root",
    storage: storage,
    blacklist: [],
}

export const rootReducers = combineReducers({
    user: userReducer,
})

const persistedReducer = persistReducer(persistConfig, rootReducers)


const store = configureStore({
    reducer: persistedReducer,
    // get rid of non-serializable values warning
    middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
})
setupListeners(store.dispatch)
export const persistor = persistStore(store)
export default store