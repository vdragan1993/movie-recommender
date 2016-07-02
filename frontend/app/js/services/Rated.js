module.exports = function ($http, $rootScope) {
    return {
        
        // load movies for dropdowns
        load: function (number) {
             return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/defaults/' + number + '/'
            });
        },

        // send recommendations
        send: function (rated, heuristic) {
            if (!heuristic){
                heuristic = 'empty';
            }
            
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/rated/',
                data: {
                    rated: rated,
                    heuristic: heuristic
                }
            });
            
        },

        // registered services (heuristics)
        services: function (user_id) {
             return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/heuristics/' + user_id + '/'
            });
        }


    };
};