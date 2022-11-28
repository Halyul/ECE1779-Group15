import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
    name: "user",
    initialState: {
        token: null,
        username: null,
        role: null,
    },
    reducers: {
        login: (state, actions) => {
            // Redux Toolkit allows us to write "mutating" logic in reducers. It
            // doesn't actually mutate the state because it uses the Immer library,
            // which detects changes to a "draft state" and produces a brand new
            // immutable state based off those changes
            console.log(actions)
            state.token = 123
            state.username = "test"
            state.role = "admin"
        },
        logout: (state) => {
            state.token = null
            state.username = null
            state.role = null
        },
    },
})

// Action creators are generated for each case reducer function
export const { login, logout } = userSlice.actions

export default userSlice.reducer