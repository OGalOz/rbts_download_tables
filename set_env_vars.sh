
chome=$PWD
impl=$PWD/lib/rbts_download_tables/rbts_download_tablesImpl.py
tst=$PWD/test/rbts_download_tables_server_test.py
tmp_dir=$PWD/test_local/workdir/tmp/
ret_dir=$PWD/test_local/workdir/tmp/ret_dir
ui_dir=$PWD/ui/narrative/methods/run_rbts_download_tables/
uspec=$PWD/ui/narrative/methods/run_rbts_download_tables/spec.json
udisp=$PWD/ui/narrative/methods/run_rbts_download_tables/display.yaml


#Docker fix
docker run -it -v /var/run/docker.sock:/run/docker.sock alpine chmod g+w /run/docker.sock

# clean up
find . -name '.DS_Store' -type f -delete
