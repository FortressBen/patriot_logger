import streamlit_authenticator as stauth
hasher = stauth.Hasher()
print(hasher.hash_list([
    'BigDawg86','MannUp25'
]))

