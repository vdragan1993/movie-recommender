module.exports = function ($http, $rootScope) {
    return {
        
        // display user profile
        display: function (user_id) {
             return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/profile/' + user_id + '/'
            });
        },

        // delete service
        delete: function (service_id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/delete/' + service_id + '/'
            });
        },

        // new service
        insert: function (service, user_id) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/insert/',
                data: {
                    service: service,
                    user: user_id
                }
            });
        },

        // edit current service
        edit: function (service) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/edit/',
                data: {
                    service: service
                }
            });
        }


    };
};