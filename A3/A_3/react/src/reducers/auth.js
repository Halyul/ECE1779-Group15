import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
    name: "user",
    initialState: {
        refreshToken: null,
        idToken: null,
        accessToken: null,
        username: null,
        role: null,
    },
    reducers: {
        successfulLogin: (state, actions) => {
            // Redux Toolkit allows us to write "mutating" logic in reducers. It
            // doesn't actually mutate the state because it uses the Immer library,
            // which detects changes to a "draft state" and produces a brand new
            // immutable state based off those changes
            state.accessToken = actions.payload.accessToken
            state.idToken = actions.payload.idToken
            state.refreshToken = actions.payload.refreshToken
            state.username = actions.payload.username
            state.role = actions.payload.role
        },
        successfulLogout: (state) => {
            state.accessToken = null
            state.idToken = null
            state.refreshToken = null
            state.username = null
            state.role = null
        },
    },
})

// Action creators are generated for each case reducer function
export const { successfulLogin, successfulLogout } = userSlice.actions

export default userSlice.reducer