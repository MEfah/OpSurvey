import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserInfo } from "../../schemas/UserInfo";

const initialState: UserInfo = {
  id: '',
  name: ''
};

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<UserInfo>) {
      return {...action.payload};
    },
    clearUser(state) {
      return {...initialState};
    }
  }
});

export default userSlice.reducer;