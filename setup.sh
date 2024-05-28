mkdir -p ~/.streamlit/

echo "
[server]
headless = true
enableCORS = true
port = $PORT
[client]
showErrorDetails = false
toolbarMode = \"viewer\"
showSidebarNavigation = true
[theme]
base = \"light\"
[ui]
hideTopBar = true
" > ~/.streamlit/config.toml