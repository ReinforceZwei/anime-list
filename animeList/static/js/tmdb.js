/* Requesting The movie DB for getting anime cover or poster image */

/*
* Search query:
* https://api.themoviedb.org/3/search/multi?api_key=73b642f3b6daaaf69b46bd8fcb98a02d&language=zh-TW&query=
*/

!function(window, $) {
    self = {}

    const API_KEY = "73b642f3b6daaaf69b46bd8fcb98a02d";
    let baseUrl = '';

    setup();

    function setup(){
        $.get(`https://api.themoviedb.org/3/configuration?api_key=${API_KEY}`)
        .done(data => {
            //console.log(data);
            baseUrl = data.images.secure_base_url
        })
    }

    function getFullImage(path){
        return baseUrl + "original" + path
    }

    self.smartSearch = function smartSearch(name){
        function _search(name){
            return new Promise((resolve, reject) => {
                search(name)
                .done(data => {
                    resolve(data);
                })
                .fail((e) => {
                    reject(e)
                })
            })
        }
        return new Promise(async (resolve, reject) => {
            let found = false;
            let count = 0; // Count how many time until found
            do {
                count++;
                result = await _search(name)

                if (result.total_results > 0){
                    result.results.forEach(e => {
                        if (e.original_language == 'ja' && e.genre_ids.includes(16)){
                            console.log("Loops spended to find the cover:", count)
                            found = true;
                            // Resolve it directly
                            resolve([getFullImage(e.poster_path), getFullImage(e.backdrop_path)])
                            return;
                        }
                    })
                }

                if (found){
                    break;
                }

                if (name.length < 3){ // Too short
                    found = false;
                    break;
                }
                name = name.substring(0, name.length - 1)
            } while (!found)
            if (!found)
                reject("No result")
        })
    }

    function search(name){
        return $.get(`https://api.themoviedb.org/3/search/multi?api_key=${API_KEY}&language=zh-TW&query=${encodeURI(name)}`)
    }

    window.tmdb = self;
}(window, $)