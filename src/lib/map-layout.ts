/** Reserve room for glass controls while leaving a usable map viewport. */
export function mapPadding(width:number,height:number,detailsHeight=0) {
  if(width<=760){
    const top=Math.min(190,height*.25);
    return {top,left:24,right:24,bottom:Math.min(Math.max(0,height-top-140),detailsHeight?detailsHeight+82:200)};
  }
  return {top:Math.min(190,height*.25),bottom:Math.min(170,height*.2),left:Math.min(370,width*.32),right:65};
}
