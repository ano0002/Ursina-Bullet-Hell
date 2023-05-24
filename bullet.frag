#version 430

uniform sampler2D tex;
uniform vec4 team1_color;
uniform vec4 team2_color;
uniform vec3 points[1000];
uniform vec3 camera_position;
uniform float bullets_size;
in vec2 uv;
uniform vec2 window_size;
out vec4 color;
void main() {
    float aspect = window_size.x/window_size.y;
    vec2 new_uv = uv-vec2(camera_position.x*0.351,camera_position.y*0.63)/camera_position.z;
    new_uv.x *= aspect;
    for (int i = 0; i < 1000; i++) {
        vec2 point1 = points[i].xy+vec2(0.5,0.5);
        point1.x *= aspect;

        float d = distance(point1,new_uv);
        if (d < bullets_size) {
            if (points[i].z == 0) {
                color = mix(team1_color, texture(tex, uv), d*(1/bullets_size));
                return;
            }
            else{
                color = mix(team2_color, texture(tex, uv), d*(1/bullets_size));
                return;
            }
        }
    }
    color = texture(tex, uv);
}