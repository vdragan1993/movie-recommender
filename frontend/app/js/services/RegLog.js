module.exports = function ($http, $rootScope) {
    return {
        // register new user
        register: function (username, email, password) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/register/',
                data: {
                    username: username,
                    email: email,
                    password: password
                }
            });
        },
        
        login: function (username, password) {
            return $http({
                method: 'POST',
                url: 'http://localhost:8000/api/login/',
                data: {
                    username: username,
                    password: password
                }
            });
        },

        isLogged: function () {
            return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/logged/'
            });
        },

        logout: function (user_id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:8000/api/logout/' + user_id + '/'
            });
        },

        hasStoredCredentials: function () {
            return $rootScope.logged === 'user';
        },

        storeCredentials: function (user, logged) {
            $rootScope.user = user;
            $rootScope.logged = logged;
        }

    };
};