ls
exit
ls
pwd
cd /root/
ls
cd files/
ls
exit
apt install imagemagick -y
apt install sed -y
sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml
exit
