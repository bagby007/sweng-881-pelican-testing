
if [ ! -d .pytest_venv ]; then
    python3 -m venv .pytest_venv
    source .pytest_venv/bin/activate
    pip3 install pytest
    pip3 install pytest-html
    pip3 install pelican
else
    echo "\n"
    echo "VENV already exists"
fi

echo "\n"
echo "-------------------------------------------"
echo "Start Env: source .pytest_venv/bin/activate"
echo "-------------------------------------------"
echo "\n"