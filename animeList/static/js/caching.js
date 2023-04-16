var db = new Dexie("AnimeDB");
var tmp_mtime = 0;

db.version(1).stores({
    anime: "animeID, animeName, addedTime, watchedTime, tags",
    mtime: 'mtime'
});
db.on('ready', () => {
    return db.anime.count(count => {
        if (count <= 0){
            console.log('Start init DB');
            return initDB()
            .then(()=>{
                console.log('Done');
            });
        } else {
            console.log('Checking data update');
            return getMtime()
            .then(mtime => {
                tmp_mtime = mtime;
                return db.mtime.where('mtime').equals(mtime).count();
            })
            .then(count => {
                if (count < 1){
                    console.log('Data have updated');
                    return initDB()
                    .then(()=>{
                        console.log('Update done');
                    })
                }else{
                    console.log('No update');
                    return setMtime(tmp_mtime);
                }
            })
        }
    });
});

db.open();
setupData()
.then(()=>{
    onDataLoad();
});

function initDB(){
    return new Promise((resolve, reject) => {
        $.get('get', {}, function (e) {
            resolve(e);
        });
    })
    .then(data => {
        return db.anime.bulkPut(data);
    })
    .then(lastKey => {
        return new Promise((resolve, reject) => {
            $.get('mtime', {}, e=>{
                resolve(e);
            });
        });
    })
    .then(mtime => {
        return setMtime(mtime);
    })
    .catch(err => {
        console.log(err);
    });
}

function setupData(){
    return db.anime.orderBy('watchedTime').reverse().toArray()
    .then(data => {
        animeList = data;
        animeList.forEach((e, i) => {
            animeListByID[e.animeID] = e;
        });
    })
}

function getMtime(){
    return new Promise((resolve, reject) => {
        $.get('mtime', {}, mtime => {
            resolve(mtime);
        })
    })
}

function setMtime(mtime){
    return db.mtime.clear()
    .then(()=>{
        return db.mtime.put({mtime: mtime});
    })
}

function updateMtime(){
    return getMtime()
    .then(mtime=>{
        return setMtime(mtime)
    })
}

function updateCache(anime){
    animeListByID[anime.animeID] = {...animeListByID[anime.animeID], ...anime};
    return db.anime.update(anime.animeID, anime)
    .then(()=>{
        return updateMtime();
    })
    .then(()=>{
        return setupData();
    })
}

function addCache(animeName, animeID){
    let id = animeID;
    let anime = {
        "animeName":animeName,
        "animeID":id,
        "addedTime":Math.floor(Date.now() / 1000),
        "downloaded":0,
        "watched":0,
        "watchedTime":0,
        "rating":0,
        "comment":"",
        "url":"",
        "remark":"",
        "tags":[]
    }
    animeListByID[id] = anime;
    return db.anime.add(anime)
    .then(()=>{
        return updateMtime();
    })
}
