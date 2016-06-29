module.exports = function ($scope, $location, $rootScope, RegLog) {
    RegLog.logout($rootScope.user.id).then(
        function (response) {
            $rootScope.user = null;
            $rootScope.logged = null;
            $location.path("/");
        }
    );

};