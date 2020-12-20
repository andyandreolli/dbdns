echo "This script installs ddget in /usr/local/bin."
read -p "Do you want to continue? (y/n) " -r

touch /usr/local/bin/ddget
ipath=$(cd $(dirname $0); pwd)
echo "python $ipath/ddget.py \${@: 1}" >> /usr/local/bin/ddget
chmod +x /usr/local/bin/ddget