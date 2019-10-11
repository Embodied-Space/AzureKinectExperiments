// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Custom/HaloEffect" {
      Properties{
          _Position("Position", Vector) = (.0, .0, .0)
          _HaloColor("Halo Color", Color) = (1.0, 1.0, 1.0, 1.0)
          _HalfWidth("Half Width", Float) = .025
          _Distance("Distance", Float) = 1.0
      }
  
      SubShader {
          Tags { "Queue"="Geometry" "Render"="Opaque" "IgnoreProjector"="True"}
          LOD 200
          
          ZWrite Off
          Blend SrcAlpha OneMinusSrcAlpha
          Cull Off
  
          Pass{
              CGPROGRAM
  
              #pragma target 3.0
              #pragma vertex vert
              #pragma fragment frag
  
              #include "UnityCG.cginc"
  
              struct appdata {
                  float4 vertex : POSITION;
                  
              };
  
              struct v2f {
                  float4 vertex : SV_POSITION;
                  float3 worldPos : TEXCOORD0;
              };
  
              uniform float3 _Position;
              uniform float4 _HaloColor;
              uniform float _HalfWidth;
              uniform float _Distance;
  
              v2f vert(appdata v) {
                  v2f o;
  
                  o.worldPos = mul (unity_ObjectToWorld, v.vertex);
                  o.vertex = UnityObjectToClipPos(v.vertex);
  
                  return o;
              }
  
              fixed4 frag(v2f i) : SV_Target {
                  float d = distance(i.worldPos, _Position);
                  if (d < _Distance - _HalfWidth || d > _Distance + _HalfWidth){
                      discard;
                  }
                  fixed4 col = _HaloColor;
                  return col;
              }
  
              ENDCG
          }
  
      
      }
      FallBack "Diffuse"
  }