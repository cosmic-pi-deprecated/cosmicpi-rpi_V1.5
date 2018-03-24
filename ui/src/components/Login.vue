<template>
<div class="col-md-6 offset-md-3 col-sm-8 offset-sm-2 ">
    <div class="card card-default">
        <div class="card-header">
            <h3>Login</h3>
        </div>
        
        <div class="card-body">
            <div v-if="!authFail" class="alert alert-warning" role="alert">
                Login is required to access to settings
            </div>
            <div v-if="authFail" class="alert alert-danger" role="alert">
                Username or password is not correct
            </div>
            <form @submit.prevent="onLoginSubmit">
                <div class="form-group">
                    <input type="text" ref="username" value="cosmicpi" class="form-control" placeholder="Username">
                </div>
                <div class="form-group">
                    <input type="password" ref="password" value="MuonsFROMSp8ce" class="form-control" placeholder="Password">
                </div>
                <button type="submit" ref="submit" class="btn btn-primary btn-lg btn-block">Login</button>
            </form>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue';


export default {
    name: 'Login',
    data() {
        return {
            authFail: false,
        }
    },
    methods: {
        getToken(user, pass) {
            return user + '_' + pass;
        },
        enable(enabled) {
            this.$refs.username.disabled = !enabled;
            this.$refs.password.disabled = !enabled;
            this.$refs.submit.disabled = !enabled;
        },
        onLoginSubmit() {
            let params = {
                token: this.getToken(this.$refs.username.value, this.$refs.password.value),
            }

            this.enable(false);
            Vue.http.get('auth', { params }).then(response => {
                this.enable(true);
                if (response.status === 200) {
                    this.authFail = false;
                    this.$store.commit('setAuth', params.token);
                } else {
                    this.authFail = true;
                }
            }).catch(() => {
                this.enable(true);
                this.authFail = true;
            });
        }
    },
}
</script>
