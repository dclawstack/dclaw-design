export interface LayerData {
  id: string;
  type: "text" | "shape" | "image" | "group";
  name: string;
  transform: {
    x: number;
    y: number;
    width: number;
    height: number;
    rotation: number;
  };
  style: {
    fill?: string;
    stroke?: string;
    strokeWidth?: number;
    fontFamily?: string;
    fontSize?: number;
    fontWeight?: string;
    opacity?: number;
  };
  content?: string | null;
  ai_generated?: boolean;
  ai_prompt?: string | null;
}

export interface ArtboardData {
  id: string;
  width: number;
  height: number;
  bg_color: string;
  layers: LayerData[];
}
