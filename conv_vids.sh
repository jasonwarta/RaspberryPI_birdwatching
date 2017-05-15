#!/bin/bash

function cleanup {
        exit
}
trap cleanup SIGHUP SIGINT SIGKILL SIGTERM SIGSTOP

cd /var/www/vids/
for f in *.h264; do
        if lsof "$f">/dev/null; then
                echo "\"$f\" was being used by a different process"
        else
                fname="$(sed 's/.h264$//'<<<"$f")";
                mv "$f" "temp.h264" &&
                MP4Box -add temp.h264 out.mp4 2>&1 >/dev/null &&
                mv out.mp4 "$fname.mp4" &&
                rm "temp.h264" &&
                echo "done processing $f"
        fi
done

