cd atomisator.db
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist

cd atomisator.feed
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd atomisator.main
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd atomisator.parser
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd pbp.buildbotenv
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd pbp.recipe.noserunner
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd pbp.recipe.trac
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd pbp.scripts
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

cd pbp.skels
python setup.py egg_info -RDb "" mregister sdist mupload -r "book"
rm -rf *egg-info build dist    

