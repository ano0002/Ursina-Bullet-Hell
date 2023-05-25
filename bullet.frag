#version 430

float distance_from_center(vec2 v){
    return length(v - vec2(0.5));
}

vec2 CRTCurveUV( vec2 uv )
{
    uv = uv * 2.0 - 1.0;
    vec2 offset = abs( uv.yx ) / vec2( 6.0, 4.0 );
    uv = uv + uv * offset * offset;
    uv = uv * 0.5 + 0.5;
    return uv;
}

void DrawVignette( inout vec4 color, vec2 uv )
{    
    float vignette = uv.x * uv.y * ( 1.0 - uv.x ) * ( 1.0 - uv.y );
    vignette = clamp( pow( 16.0 * vignette, 0.3 ), 0.0, 1.0 );
    color *= vignette;
}

void DrawScanline( inout vec4 color, vec2 uv )
{
    float scanline 	= clamp( 0.95 + 0.05 * cos( 3.14 * ( uv.y + 0.008  ) * 240.0 * 1.0 ), 0.0, 1.0 );
    float grille 	= 0.85 + 0.15 * clamp( 1.5 * cos( 3.14 * uv.x * 640.0 * 1.0 ), 0.0, 1.0 );    
    color *= scanline * grille * 1.2;
}

uniform sampler2D tex;
uniform vec4 team1_color;
uniform vec4 team2_color;
uniform vec3 points[1000];
uniform vec3 camera_position;
uniform float bullets_size;
uniform float vignette_distance;
uniform vec4 vignette_color;
uniform float vignette_density;
in vec2 uv;
uniform vec2 window_size;
out vec4 color;
void main() {
    float aspect = window_size.x/window_size.y;
    vec2 curved_uv = CRTCurveUV(uv);
    vec2 new_uv = curved_uv-vec2(camera_position.x*0.351,camera_position.y*0.63)/camera_position.z;
    new_uv.x *= aspect;
    color = texture(tex, curved_uv);
    for (int i = 0; i < 1000; i++) {
        vec2 point1 = points[i].xy+vec2(0.5,0.5);
        point1.x *= aspect;
        if (points[i].y < 0.5 && points[i].y > -0.5) {
            float d = distance(point1,new_uv);
            if (d < bullets_size) {
                if (points[i].z == 0) {
                    color = mix(team1_color, color, d*(1/bullets_size));
                }
                else{
                    color = mix(team2_color, color, d*(1/bullets_size));
                }
            }

        }
    }
    DrawVignette(color, uv);
    DrawScanline(color, uv);
}