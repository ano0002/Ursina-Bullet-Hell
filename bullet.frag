#version 430

uniform sampler2D tex;
uniform vec4 fireflies_color;
uniform vec2 points[1000];
uniform vec3 camera_position;
uniform float fireflies_size;
in vec2 uv;
uniform vec2 window_size;
out vec4 color;
void main() {
    float aspect = window_size.x/window_size.y;
    vec2 new_uv = uv-vec2(camera_position.x*0.351,camera_position.y*0.63)/camera_position.z;
    new_uv.x *= aspect;
    for (int i = 0; i < 1000; i++) {
        vec2 point1 = points[i]+vec2(0.5,0.5);
        point1.x *= aspect;

        float d = distance(point1,new_uv);
        if (d < fireflies_size) {
            color = mix(fireflies_color, texture(tex, uv), d*(1/fireflies_size));
            return;
        }
    }
    color = texture(tex, uv);
}